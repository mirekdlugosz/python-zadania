#!/usr/bin/env python3

import datetime
from pesel import PESEL

birthday = input("Podaj datę urodzenia: ")
birthday = datetime.datetime.strptime(birthday, "%d-%m-%Y")

pesel = PESEL().from_date(birthday.year, birthday.month, birthday.day)
pesel.generate()

print(pesel.to_string())
