from matching import Matching


class RGS(Matching):
    def __init__(self, h, r):
        self.h = h  # number of hospitals
        self.r = r  # number of residents

        self.hPreferences = [[] for i in range(self.h + 1)]  # hospital preference lists
        self.rPreferences = [[] for i in range(self.r + 1)]  # resident preference lists
        self.capacity = [0] * (self.h + 1)  # number of residents each hospital is willing to take
        self.hMatch = [[] for i in range(self.h + 1)]  # current match of hospitals, all initialized as unmatched
        self.rMatch = [0] * (self.r + 1)  # current match of residents, all initialized as unmatched

        self.nextProposal = [0] * (self.r + 1)
        # each resident will propose to this hospital index in their preference list next
        # r1 will propose to the hospital whose index is held in nextProposal[1]
        # set to 0 initially meaning that proposals start from the top of the preference list

    # finds the least preferred resident currently matched to a specific hospital
    def findWorstResident(self, match, preferences):
        worstResident = match[0]
        worstResidentRank = preferences.index(match[0])
        for resident in match:
            if preferences.index(resident) > worstResidentRank:
                worstResident = resident
                worstResidentRank = preferences.index(resident)
        return worstResident

    def algorithm(self, splitHospitals, splitResidents, capacities):
        # An extension of the Gale-Shapley algorithm to the Hospital-Residents Problem
        # Resident-Oriented GS (RGS)

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

        # at first, some free resident who hasn't proposed to every acceptable hospital must exist
        freeProposerExists = True
        resident = 1  # we assume resident 1 is free
        steps = []
        while freeProposerExists:
            freeProposerExists = False
            if self.nextProposal[resident] == len(self.rPreferences[resident]):
                # resident has proposed to all acceptable hospitals, will now remain unmatched
                steps.append(f"Resident {resident} has proposed to all acceptable hospitals, will remain unmatched")
                self.rMatch[resident] = -1
            else:
                # index of the next hospital the resident has not proposed to yet
                nextProposalIndex = self.nextProposal[resident]
                # the next hospital the resident hasn't proposed to yet
                hospital = self.rPreferences[resident][nextProposalIndex]
                self.nextProposal[resident] += 1  # move index to the next hospital in the list
                if resident in self.hPreferences[hospital]:
                    # matching resident to first hospital on their list that finds them acceptable
                    steps.append(f"Resident {resident} is matched to Hospital {hospital}")
                    self.rMatch[resident] = hospital
                    self.hMatch[hospital].append(resident)
                    seatsFilled = len(self.hMatch[hospital])
                    if seatsFilled > self.capacity[hospital]:
                        # if the capacity is exceeded, we remove the least preferred resident currently matched
                        worstResident = self.findWorstResident(self.hMatch[hospital], self.hPreferences[hospital])
                        self.rMatch[worstResident] = 0
                        steps.append(f"Capacity exceeded,"
                                     f" removing Resident {worstResident} from matches of Hospital {hospital}")
                        self.hMatch[hospital].remove(worstResident)
                    elif seatsFilled == self.capacity[hospital]:
                        # as the hospital capacity is reached, it will not accept anyone worse than the current worst
                        steps.append("Capacity reached")

                        # finding the worst resident currently matched to the hospital
                        worstResident = self.findWorstResident(self.hMatch[hospital], self.hPreferences[hospital])
                        i = 0
                        while self.hPreferences[hospital][i] != worstResident:
                            i += 1
                        i += 1
                        # for each resident that is lower in the hospital's preference list than the worst resident
                        # we remove the hospital, so residents will not make proposals that will obviously be rejected
                        while i < len(self.hPreferences[hospital]):
                            residentToRemove = self.hPreferences[hospital][i]
                            if hospital in self.rPreferences[residentToRemove]:
                                steps.append(f"Removing Hospital {hospital} from list of Resident {residentToRemove}")
                                self.rPreferences[residentToRemove].remove(hospital)
                            i += 1
                else:
                    # proposal rejected, continue with current resident, so they can make a new proposal
                    steps.append("Hospital rejects")
                    freeProposerExists = True
                    continue

            # finding a free resident
            resident = self.nextFreeProposer(self.rMatch, self.r)
            if resident != 0:
                freeProposerExists = True

        self.printHRMatching(self.rMatch, self.r)
        return self.rMatch, steps
