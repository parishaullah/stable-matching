from matching import Matching


class HGS(Matching):
    def __init__(self, h, r):
        self.h = h  # number of hospitals
        self.r = r  # number of residents

        self.hPreferences = [[] for i in range(self.h + 1)]  # hospital preference lists
        self.rPreferences = [[] for i in range(self.r + 1)]  # resident preference lists
        self.capacity = [0] * (self.h + 1)  # number of residents each hospital is willing to take
        self.full = [False] * (self.h + 1)  # whether a hospital is full or not
        self.hMatch = [[] for i in range(self.h + 1)]  # current match of hospitals, all initialized as unmatched
        self.rMatch = [0] * (self.r + 1)  # current match of residents, all initialized as unmatched

        self.nextProposal = [0] * (self.h + 1)
        # each hospital will propose to this resident index in their preference list next
        # h1 will propose to the resident whose index is held in nextProposal[1]
        # set to 0 initially meaning that proposals start from the top of the preference list

    # returns index of first hospital who is unmatched and has a non-empty list
    def nextFreeProposerWithoutEmptyList(self):
        for i in range(1, self.h + 1):
            if not self.full[i] and len(self.hPreferences[i]) != 0:
                return i
        return 0

    def algorithm(self, splitHospitals, splitResidents, capacities):
        # An extension of the Gale-Shapley algorithm to the Hospital-Residents Problem
        # Hospital-Oriented GS (HGS)

        # taking input for each hospital's preference list
        for i in range(1, self.h + 1):
            pref = splitHospitals[i - 1]
            residents = pref.split()
            for resident in residents:
                self.hPreferences[i].append(int(resident))

        # taking input for each resident's preference list
        for i in range(1, self.r + 1):
            pref = splitResidents[i - 1]
            hospitals = pref.split()
            for hospital in hospitals:
                self.rPreferences[i].append(int(hospital))

        #  taking input for each hospital's capacity
        i = 1
        for capacity in capacities:
            self.capacity[i] = int(capacity)
            i += 1

        # at first, some hospital that is undersubscribed and has a nonempty list must exist
        freeProposerExists = True
        hospital = 1  # we assume hospital 1 has seats and a nonempty list
        steps = []
        while freeProposerExists:
            freeProposerExists = False
            if self.nextProposal[hospital] == len(self.hPreferences[hospital]):
                # hospital has proposed to all acceptable residents, will now remain undersubscribed
                steps.append(f"Hospital {hospital} has proposed to all acceptable residents,"
                             f" will remain undersubscribed")
                self.full[hospital] = True
            else:
                # index of the next resident the hospital has not proposed to yet
                nextProposalIndex = self.nextProposal[hospital]
                # the next resident the hospital hasn't proposed to yet
                resident = self.hPreferences[hospital][nextProposalIndex]
                steps.append(f"Hospital {hospital} is proposing to Resident {resident}")
                self.nextProposal[hospital] += 1  # move index to the next resident in the list
                if hospital in self.rPreferences[resident]:
                    if self.rMatch[resident] != 0:
                        # we know proposals are only received from more preferred hospitals, so set previous match free
                        steps.append(f"Resident prefers Hospital {hospital},"
                                     f" previous match Hospital {self.rMatch[resident]} is set free")
                        self.hMatch[self.rMatch[resident]].remove(resident)
                        self.nextProposal[self.rMatch[resident]] -= 1
                        self.full[self.rMatch[resident]] = False

                    # proposing hospital and resident are matched
                    steps.append(f"Resident accepts")
                    self.rMatch[resident] = hospital
                    self.hMatch[hospital].append(resident)

                    # finding the index of the hospital in the resident's preference lists
                    i = 0
                    while self.rPreferences[resident][i] != hospital:
                        i += 1
                    i += 1
                    # for each hospital that is lower in the resident's preference list than the matched hospital
                    # we remove the resident, so hospitals will not make proposals that will obviously be rejected
                    while i < len(self.rPreferences[resident]):
                        hospitalToRemove = self.rPreferences[resident][i]
                        if resident in self.hPreferences[hospitalToRemove]:
                            steps.append(f"Removing Resident {resident} from list of Hospital {hospitalToRemove}")
                            self.hPreferences[hospitalToRemove].remove(resident)
                        i += 1

                    if len(self.hMatch[hospital]) == self.capacity[hospital]:
                        # hospital has met capacity, so set it as full
                        self.full[hospital] = True
                else:
                    # proposal rejected, continue with current hospital, so it can make a new proposal
                    steps.append("Resident rejects")
                    freeProposerExists = True
                    continue

            # finding a free hospital
            hospital = self.nextFreeProposerWithoutEmptyList()
            if hospital != 0:
                freeProposerExists = True

        self.printHRMatching(self.rMatch, self.r)
        return self.rMatch, steps
