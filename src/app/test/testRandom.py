"""file that runs all tests for the random module."""

from .. import random

def main():
    """Runs all random module tests."""

    print("   Test CheckLogisticRemoval()...")
    testCheckLogisticRemoval()

def testCheckLogisticRemoval():
    """Tests the checkLogisticRemoval function."""
    totalrunsPerScore = 10000

    for score in range(0, 50):
        print ("    Testing Value: " + str(score))
        count = 0
        for numRuns in range(0, totalrunsPerScore):
            if random.checkLogisticRemoval(score) == False:
                count += 1

        if score == 0 or score == 1:
            idealScore = totalrunsPerScore
        else:
            idealScore = totalrunsPerScore/score

        assert count >= idealScore*0.80 and count <= idealScore*1.20, "Value: " + str(score) + " Ideal: " + str(idealScore) + " Actual: " + str(count)
