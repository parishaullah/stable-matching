from matching import Matching


class SMI(Matching):
    def __init__(self, n, leadersPropose):
        # super().__init__(n, leadersPropose)

        self.n = n  # maximum number of leaders and followers each
        self.leadersPropose = leadersPropose

        self.lPreferences = [[0 for y in range(self.n + 1)] for x in range(self.n + 1)]  # leader preference lists
        self.fPreferences = [[0 for y in range(self.n + 1)] for x in range(self.n + 1)]  # follower preference lists
        self.lMatch = [0] * (self.n + 1)  # which follower each leader is matched to, all initialized as unmatched
        self.fMatch = [0] * (self.n + 1)  # which leader each follower is matched to, all initialized as unmatched

        self.nextProposal = [0] * (self.n + 1)
        # each leader will propose to this follower index in their preference list next
        # l1 will propose to the follower whose index is held in nextProposal[1]
        # vice versa for if followers are proposing
        # set to 0 initially meaning that proposals start from the top of the preference list

    def algorithm(self, splitLeaders, splitFollowers):
        # Extension of Gale-Shapley algorithm for incomplete lists

        # taking input for each leader's preference list
        for i in range(1, self.n + 1):
            pref = splitLeaders[i - 1]
            followers = pref.split()
            j = 0
            for follower in followers:
                self.lPreferences[i][j] = int(follower)
                j += 1

        # taking input for each follower's preference list
        for i in range(1, self.n + 1):
            pref = splitFollowers[i - 1]
            leaders = pref.split()
            j = 0
            for leader in leaders:
                self.fPreferences[i][j] = int(leader)
                j += 1

        # at first, some free proposer who hasn't proposed to every acceptable partner must exist
        freeProposerExists = True
        if self.leadersPropose:
            steps = ["Leaders are proposing"]
            # leaders are proposing to followers
            leader = 1  # we assume leader 1 is free
            while freeProposerExists:
                freeProposerExists = False
                # index of the next follower the leader has not proposed to yet
                nextProposalIndex = self.nextProposal[leader]
                # the next follower the leader hasn't proposed to yet
                follower = self.lPreferences[leader][nextProposalIndex]
                if follower == 0:
                    # leader has proposed to all their acceptable partners, will now remain unmatched
                    steps.append(f"Leader {leader} has proposed to all acceptable followers, will remain unmatched")
                    self.lMatch[leader] = -1
                else:
                    steps.append(f"Leader {leader} is proposing to Follower {follower}")
                    self.nextProposal[leader] += 1  # move index to the next follower in the list
                    if self.fMatch[follower] == 0 and leader in self.fPreferences[follower]:
                        # follower is free and finds leader acceptable, engage leader and follower
                        self.fMatch[follower] = leader
                        self.lMatch[leader] = follower
                        steps.append("Follower accepts")
                    elif self.betterMatch(leader, self.fMatch[follower], self.fPreferences[follower]):
                        # follower is tentatively engaged, so we should check if they prefer leader to their partner
                        # since it's a better match, engage leader and follower
                        # set follower's previous partner as free
                        steps.append(f"Follower prefers Leader {leader},"
                                     f" previous match Leader {self.fMatch[follower]} is set free")
                        self.lMatch[self.fMatch[follower]] = 0
                        self.fMatch[follower] = leader
                        self.lMatch[leader] = follower
                    else:
                        # proposal rejected, continue with the current leader, so they can make new proposal
                        steps.append("Follower rejects")
                        freeProposerExists = True
                        continue

                # finding a free leader
                leader = self.nextFreeProposer(self.lMatch, self.n)
                if leader != 0:
                    freeProposerExists = True

            self.printMatching(self.lMatch)
            return self.lMatch, steps
        else:
            steps = ["Followers are proposing"]
            # followers are proposing to leaders
            follower = 1  # we assume follower 1 is free
            while freeProposerExists:
                freeProposerExists = False
                # index of the next leader the follower has not proposed to yet
                nextProposalIndex = self.nextProposal[follower]
                # the next leader the follower hasn't proposed to yet
                leader = self.fPreferences[follower][nextProposalIndex]
                if leader == 0:
                    # follower has proposed to all their acceptable partners, will now remain unmatched
                    steps.append(f"Follower {follower} has proposed to all acceptable leaders, will remain unmatched")
                    self.fMatch[follower] = -1
                else:
                    steps.append(f"Follower {follower} is proposing to Leader {leader}")
                    self.nextProposal[follower] += 1  # move index to the next leader in the list
                    if self.lMatch[leader] == 0 and follower in self.lPreferences[leader]:
                        # leader is free and finds follower acceptable, engage leader and follower
                        steps.append("Leader accepts")
                        self.fMatch[follower] = leader
                        self.lMatch[leader] = follower
                    elif self.betterMatch(follower, self.lMatch[leader], self.lPreferences[leader]):
                        # leader is tentatively engaged, so we should check if they prefer follower to their partner
                        # since it's a better match, engage leader and follower
                        # set leader's previous partner as free
                        steps.append(f"Leader prefers Follower {follower},"
                                     f" previous match Follower {self.lMatch[leader]} is set free")
                        self.fMatch[self.lMatch[leader]] = 0
                        self.fMatch[follower] = leader
                        self.lMatch[leader] = follower
                    else:
                        # proposal rejected, continue with the current follower, so they can make new proposal
                        steps.append("Leader rejects")
                        freeProposerExists = True
                        continue

                # finding a free follower
                follower = self.nextFreeProposer(self.fMatch, self.n)
                if follower != 0:
                    freeProposerExists = True

            self.printMatching(self.fMatch)
            return self.fMatch, steps
