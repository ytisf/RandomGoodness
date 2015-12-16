#!/usr/bin/python

"""
This little script uses the Complements Method to subtract two numbers
with addition and without subtraction. Just a fun toy.
"""

# Two inputs
a = "11031952"
b = "42"

# Empty array for the converted number
arr = []

# 2nd number is bigger i'm flipping them
if int(a) < int(b):
    backup = a
    a = b
    b = backup
    backup = None

print "\n\nWill now substract (%s with %s)." % (a, b)

# Checking if there is a difference.
if len(a) == len(b):
    print "Both numbers are with length %s." % len(a)
else:
    if len(a) > len(b):
        diff = len(a) - len(b)
        print "%s has %s digits less than %s." % (b, diff, a)

# Adding the 9's
try:
    for i in range(0, diff):
        arr.append('9')
    print "Added %d '9's to match length." % diff
except:
    pass

c = list(b)     # Convert 2nd number into a char array
d = list(a)     # Convert 1st number into a char array

# Convert all the digits but the last one
for digit in c[:-1]:
    this_digit = 9-int(digit)
    arr.append(this_digit)

# Last digit
this_digit = 10-int(c[-1])

# Check if both numbers trail with 0
if int(this_digit) == 10 and int(d[-1]) == 0:
    arr[-1] += 1
    arr.append("0")
else:
    arr.append(this_digit)

# Combining the number together
converted_number = ""
for i in arr:
    converted_number += str(i)
print "%s is now %s" % (b, converted_number)

add_result = str(int(a) + int(converted_number))

print ""
print str(a) + "+"
print str(converted_number)
print "-"*(len(add_result)+3)
print "%s \t\t# Dropped an extra %s\n" % (add_result[1:], add_result[1])
