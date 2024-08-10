class Matching:
    def __init__(self, n, leadersPropose):
        pass

    # returns true if f prefers l to their partner l' or vice versa for followers proposing
    def betterMatch(self, l, lPrime, fPreference):
        for leader in fPreference:
            if leader == lPrime:
                return False
            if leader == l:
                return True

    # return index of first proposer who is unmatched
    def nextFreeProposer(self, match, n):
        for i in range(1, n + 1):
            if match[i] == 0:
                return i
        return 0

    # print the pairs of the stable matching produced
    def printMatching(self, match):
        if self.leadersPropose:
            print("l  f")
        else:
            print("f  l")
        for i in range(1, self.n + 1):
            print("{}, {}".format(i, match[i]))

    # print hospital-resident pairs
    def printHRMatching(self, match, r):
        print("r h")
        for i in range(1, r + 1):
            print("{}, {}".format(i, match[i]))
