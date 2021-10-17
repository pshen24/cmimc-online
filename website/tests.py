#from django.test import TestCase
import models.py
import registration.py

def validate(self, user_input):
    '''
    Checks if the user input is a
    '''
    lines = user_input.split("\n")
    noDupes = set()
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            return False
        for part in parts: # Checks if it's actually integer
            try: 
                int(part)
            except ValueError:
                return False
        a = int(parts[0])
        b = int(parts[1])
        if (1 > a) or (a >= b) or (b > self["n"]):
            return False
        # Checking for dupes
        # Note that n(a - 1) + b - 1 is a bijective mapping
        x = self["n"] * (a - 1) + b - 1
        if x in noDupes:
            return False
        noDupes.add(x)
    return True

self = {}
self["n"] = 4
x = "1 3\n1 2"
y = x.split("\n")
for line in y:
    print(line.split())


print(validate(self, x))


# Create your tests here.
nin = Team()