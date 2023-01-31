from itertools import permutations
from math import comb

all_letters = "abcdefghijklmnopqrstuvwxyz"
perms = list(permutations(all_letters, 5))
success = 0

for prompt in perms:
    letters = all_letters
    placed = []
    attempt = "?????"
    failure = 0
    for call in prompt:
        # Determine which slots are eligible for the letter that is called out
        eligible = []

        for slot in range(5):

            # if the slot is already taken, it is ineligible
            if attempt[slot] != "?":
                continue

            # check the latest letter alphabetically in the positions to the left of the considered slot
            # check the earliest letter alphabetically in the positions to the right of the considered slot
            left = attempt[:slot].replace("?", "")
            right = attempt[slot+1:].replace("?", "")

            # if the called letter comes alphabetically before the latest letter to its left, the slot is ineligible
            if len(left) != 0:
                left = max(left)
                if left > call:
                    continue

            # if the called letter comes alphabetically after the earliest letter to its right, the slot is ineligible
            if len(right) != 0:
                right = min(right)
                if right < call:
                    continue

            # if none of those conditions are met, the slot is eligible; add it to the list of eligible positions
            eligible.append(slot)

        # if zero slots are eligible, this attempt at the challenge is a failure; move on to the next prompt
        if len(eligible) == 0:
            failure = 1
            break

        best_slot = best_outcomes = -1

        for slot in eligible:

            # Determine which eligible slot is optimal by counting the number of successful outcomes it would yield
            # For a success, the number of slots before the considered slot must match
            #   the number of called letters alphabetically before the current call
            # Similarly, the number of slots after the considered slot must match
            #   the number of called letters alphabetically after the current call
            left = comb(letters.index(call), attempt[:slot].count("?"))
            right = comb(len(letters) - 1 - letters.index(call), attempt[slot:].count("?") - 1)

            outcomes = left*right

            # Use the current slot if it would lead to more successful outcomes than the previous best slot
            if outcomes > best_outcomes:
                best_outcomes = outcomes
                best_slot = slot

        # Place the called letter in its best possible slot
        attempt = attempt[:best_slot] + call + attempt[best_slot+1:]

        # Add the called letter to the placed guesses list, and remove it from the alphabet string
        placed.append(call)
        letters = letters[:letters.index(call)] + letters[letters.index(call)+1:]

    # if no failure states were generated, count the attempt as successful
    success += 1 - failure

# print the result
print(str(round(success/len(perms)*100, 4))+"%")
