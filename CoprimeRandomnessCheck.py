#!/usr/local/bin/python3

"""
This will get a random dataset of numbers in pairs ( [[1,2].[2,3]...] )
and will put them in a pools or coprimes or cofactors and then asses how
close that is to (6/(pi^2)).
"""

import random

from math import gcd as bltin_gcd
from math import pi

DICE_ROLL = 10**6
MAX_INT = 10**9


def _coprime2(a, b):
    return bltin_gcd(a, b) == 1

def DiceRoll():
    tho = []
    print("Rolling the dice %s times." % DICE_ROLL)
    for i in range(1, DICE_ROLL+1):
        tho.append([random.randint(1,MAX_INT),random.randint(1,MAX_INT)])
    print("Done roling the dice. Got %s pairs." % len(tho))
    return(tho)


def logic():
    coprime_count = 0
    cofactor_count = 0

    tho = DiceRoll()
    print("Sorting coprimes and cofactors...")
    for a,b in tho:
        if _coprime2(a,b):
            coprime_count += 1
        else:
            cofactor_count += 1
    print("Data:")
    print("\tCoprimes count: \t%s" % coprime_count)
    print("\tCofactors count: \t%s" % cofactor_count)
    print("\tRatio of coprimes: \t%s" % (coprime_count/DICE_ROLL))
    print("\t----------------------------------")
    print("\tRATIO IN DATASET: \t%s" % (coprime_count/DICE_ROLL))
    print("\t6/pi^2: \t\t%s" % (str(6/(pi**float(2)))[:8]))
    ratio = ((6/(pi**float(2)) / coprime_count/DICE_ROLL))
    p_ratio = "{:.10%}".format(ratio)
    print("\tMargin of Error: \t%s" % p_ratio)


if __name__ == "__main__":
    logic()
