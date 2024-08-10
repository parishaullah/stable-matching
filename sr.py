from matching import Matching


class SR(Matching):
    def __init__(self, n):
        # super().__init__(n, leadersPropose)

        self.n = n  # maximum number of leaders and followers each
        self.preferences = [[] for i in range(self.n + 1)]  # preference lists
        self.match = [0] * (self.n + 1)  # who each agent is semiengaged to, all initialized as unmatched

    # returns index of first agent  who is unmatched and has a non-empty list
    def nextFreeProposerWithoutEmptyList(self, match, preferences, n):
        for i in range(1, self.n + 1):
            if match[i] == 0 and len(preferences) != 0:
                return i
        return 0

    # returns index of first agent who has multiple entries in their preferences
    def findListInSecondPhase(self, table):
        for i in range(1, self.n + 1):
            if len(table[i]) > 1:
                return i
        return 0

    # checks if all preference lists have at least one entry
    def allListsNonEmpty(self, table):
        for i in range(1, self.n + 1):
            if len(table[i]) == 0:
                return False
        return True

    def algorithm(self, splitPreferences):
        # Irving's algorithm for stable roommates

        # taking input for each person's preference list
        for i in range(1, self.n + 1):
            pref = splitPreferences[i - 1]
            people = pref.split()
            for person in people:
                self.preferences[i].append(int(person))

        # Phase 1 of the algorithm
        # at first, some free person who hasn't proposed to everyone they find acceptable must exist
        freeProposerExists = True
        proposer = 1  # we assume person 1 is free
        steps = ["Phase 1"]
        while freeProposerExists:
            freeProposerExists = False
            responder = self.preferences[proposer][0]  # the next person the proposer prefers the most
            if responder in self.match:
                # someone is semiengaged to this person, set that person free
                # as people only get proposals from better matches, we know the proposer is more preferred
                steps.append(
                    f"Person {self.match.index(responder)} was semiengaged to Person {responder}, now set free")
                self.match[self.match.index(responder)] = 0
            # proposer is semiengaged to the person they have proposed to
            steps.append(f"Person {proposer} is semiengaged to Person {responder}")
            self.match[proposer] = responder

            # for every successor of the proposer in the responder's list
            # we remove the responder, so they will not receive a proposal any worse than the one they have right now
            for person in reversed(self.preferences[responder]):
                if person == proposer:
                    break
                steps.append(f"Removing Person {person} and Person {responder} from each other's preference lists")
                self.preferences[person].remove(responder)
                self.preferences[responder].remove(person)

            # finding a free proposer
            proposer = self.nextFreeProposerWithoutEmptyList(self.match, self.preferences, self.n)
            if proposer != 0:
                freeProposerExists = True

        for i in range(1, self.n + 1):
            print("{}, {}".format(i, self.match[i]))

        for i in range(1, self.n + 1):
            print(self.preferences[i])

        # Phase 2 of the algorithm
        steps.append("Phase 2")
        # preference lists have now become the phase 1 table
        person = self.findListInSecondPhase(self.preferences)
        instanceSolvabale = self.allListsNonEmpty(self.preferences)
        while person and instanceSolvabale:
            # find a rotation phi exposed in T
            p = [person]
            q = [self.preferences[person][1]]  # second preference of person
            while self.preferences[q[-1]][-1] not in p:
                p.append(self.preferences[q[-1]][-1])  # last preference of person in q
                q.append(self.preferences[p[-1]][1])  # second preference of person in p
            p.append(self.preferences[q[-1]][-1])

            # remove exposed rotation from T
            i = p.index(p[-1])
            while i < len(q):
                steps.append(f"Removing Person {q[i]} and Person {p[i + 1]} from each other's preferences")
                # delete p(i+1) from qi's list
                self.preferences[q[i]].remove(p[i + 1])
                # delete qi from p(i+1)'s list
                self.preferences[p[i + 1]].remove(q[i])
                i += 1

            person = self.findListInSecondPhase(self.preferences)
            instanceSolvabale = self.allListsNonEmpty(self.preferences)

        if not instanceSolvabale:
            steps.append("Instance has no stable matching")
        else:
            # table is the stable matching
            for i in range(1, self.n + 1):
                print(self.preferences[i])
                self.match[i] = self.preferences[i][0]

        return self.match, steps, instanceSolvabale
