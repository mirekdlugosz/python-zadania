# -*- coding: utf-8 -*-
from __future__ import print_function

import random

try:
    input = raw_input
except NameError:
    pass

def generate_nip():
    weights = (6,5,7,2,3,4,5,6,7)

    while True:
        numbers = [
                    random.randint(1,9),
                    random.randint(0,9),
                    random.randint(1,9),
                    random.randint(0,9),
                    random.randint(0,9),
                    random.randint(0,9),
                    random.randint(0,9),
                    random.randint(0,9),
                    random.randint(0,9)
                ]
        control_number = sum([i * j for i,j in zip(numbers, weights)]) % 11
        if control_number < 10:
            break

    numbers.append(control_number)

    return "".join(map(str,numbers))

if __name__ == "__main__":
    answer = None
    while answer != "n":
        print(generate_nip())
        answer = input("Wygenerować kolejny numer? [t]/n ")
