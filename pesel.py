"""PESEL number handler.

PESEL class extracts basic information from PESEL number - date
of birth and number itself. Main use cases are:

    * Retrieving date of birth from number
    * Generating new number based on date of birth
    * Number validation

Examples
--------

    pesel = PESEL().from_string("16111012344")
    print(pesel.to_date("%d %m %Y"))

    pesel = PESEL().from_date(year=2016, month=11, day=2)
    pesel.generate()
    print(pesel.to_string())

"""


import datetime
import random

class PESEL():
    """Main PESEL class.
    """

    def __init__(self):
        self.__centuries = (1900, 2000, 2100, 2200, 1800)
        self.__min_date = datetime.datetime(year=1800, month=1, day=1)
        self.__max_date = datetime.datetime(year=2299, month=12, day=31)
        self.date = None
        self.number = None

    def from_string(self, string):
        """Creates PESEL object from PESEL number given as string.

        Performs following validation tests before creating object:

        * Length of given string (must be 11 characters)
        * Used characters (only digits are allowed)
        * Date of birth exists
        * Computes control number and compares it to one provided

        Raises ValueError exception if any check does not pass.

        Args:
            string: PESEL number as string

        Returns:
            PESEL object instance
        """
        if len(string) != 11:
            raise ValueError("String must be exactly 11 characters long; {0} is {1}".format(
                string, len(string)))

        if not string.isnumeric():
            raise ValueError("{} contains illegal characters".format(string))

        year  = int(string[0:2])
        month = int(string[2:4])
        day   = int(string[4:6])

        century_index, month = divmod(month, 20)
        year = self.__centuries[ century_index ] + year

        self.date = datetime.datetime(year=year, month=month, day=day)

        self.number = string
        self.__verify_control_number()
        return self

    def from_date(self, year, month, day):
        """Creates PESEL object from date of birth

        Performs following validation tests before creating object:

        * Date of birth exists
        * Year of birth falls into range 1800-2299

        Raises ValueError exception if any of checks does not pass

        Note:
            After creating PESEL object instance using from_date method,
            you should call generate method to create PESEL number for
            this instance.

        Args:
            year: Year of birth as integer
            month: Month of birth as integer
            day: Day of birth as integer

        Returns:
            PESEL object instance
        """
        self.date = datetime.datetime(year=year, month=month, day=day)

        if self.__min_date > self.date or self.date > self.__max_date:
            raise ValueError("Date out of range; PESEL number is defined for years 1800-2299")

        return self

    def generate(self):
        """Generates random (but valid) PESEL number.

        Generated number is stored as object instance property. It is
        guaranteed to be valid, but is not guaranteed to be unique.

        This method is usually called after PESEL object was created
        by from_date method. It is not called automatically to allow
        flexibility and custom implementation of uniqueness guarantee
        on top of PESEL class.

        Note:
            generate method may be called on object instances generated
            by from_string method, but it hardly makes sense. It will
            erase any reference to original PESEL number and generate
            new one with the same first six digits.

        Args:
            None

        Returns:
            None
        """
        century, year_value = divmod(self.date.year, 100)
        year_value = "{:02d}".format(year_value)

        century *= 100
        month_value = self.date.month + self.__centuries.index(century) * 20
        month_value = "{:02d}".format(month_value)
        
        day_value   = self.date.strftime("%d")

        sequence = "{:04d}".format(random.randint(0, 9999))

        numbers = "{y}{m}{d}{s}".format(**{
                "y": year_value,
                "m": month_value,
                "d": day_value,
                "s": sequence
            })

        self.number = "{numbers}{control}".format(**{
                "numbers": numbers,
                "control": self.__compute_control_number(numbers)
            })

    def to_string(self):
        """Returns PESEL number as string.
        """
        return self.number

    def to_date(self, date_format):
        """Returns date of birth as string.

        Args:
            date_format: Date format recognized by datetime.strftime method

        Returns:
            Date of birth as string formatted according to provided
            specification
        """
        return self.date.strftime(date_format)

    def __compute_control_number(self, numbers):
        """Computes valid PESEL control number from 10 digits

        Args:
            numbers: 10 characters long string containing digits only

        Returns:
            Control number, created according to PESEL specification, as integer.
            Guaranteed to be single digit.
        """
        numbers = list(map(int, numbers))
        weights = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)
        control_number = (10 - sum([i * j for i,j in zip(numbers, weights)]) % 10) % 10
        return control_number

    def __verify_control_number(self):
        """Verifies PESEL control number in stored PESEL number

        Raises ValueError exception if computed control number does not
        match one given in stored PESEL number.
        """
        given_control_number = int(self.number[-1:])
        numbers = self.number[:-1]
        computed_control_number = self.__compute_control_number(numbers)

        if given_control_number != computed_control_number:
            raise ValueError("Control number does not match in {0}; expected {1}, got {2}".format(
                self.number, computed_control_number, given_control_number))

    def __str__(self):
        return self.number
