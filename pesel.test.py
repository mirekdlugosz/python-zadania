import unittest

from pesel import PESEL

class TestFromString(unittest.TestCase):

    def test_short_string(self):
        with self.assertRaises(ValueError):
            PESEL().from_string("780524")

    def test_long_string(self):
        with self.assertRaises(ValueError):
            PESEL().from_string("78052411474985")

    def test_alpha_char(self):
        with self.assertRaises(ValueError):
            PESEL().from_string("78abc859694")

    def test_space(self):
        with self.assertRaises(ValueError):
            PESEL().from_string("78a c859694")

    def test_special_char(self):
        with self.assertRaises(ValueError):
            PESEL().from_string("7-_=+*/<>82")

    def test_zero_month(self):
        with self.assertRaises(ValueError):
            PESEL().from_string("49000501580")

    def test_zero_day(self):
        with self.assertRaises(ValueError):
            PESEL().from_string("49040001580")

    def test_invalid_month(self):
        with self.assertRaises(ValueError):
            PESEL().from_string("49140501580")

    def test_invalid_day(self):
        with self.assertRaises(ValueError):
            PESEL().from_string("49043501580")

    def test_invalid_control_number(self):
        with self.assertRaises(ValueError):
            PESEL().from_string("49040501587")

    def test_19th_century(self):
        self.assertTrue(PESEL().from_string("16911012348"))

    def test_20th_century(self):
        self.assertTrue(PESEL().from_string("16111012344"))

    def test_21st_century(self):
        self.assertTrue(PESEL().from_string("16311012340"))

    def test_22nd_century(self):
        self.assertTrue(PESEL().from_string("16511012346"))

    def test_23rd_century(self):
        self.assertTrue(PESEL().from_string("16711012342"))

class TestFromDate(unittest.TestCase):

    def test_invalid_year_below(self):
        with self.assertRaises(ValueError):
            PESEL().from_date(year=1799, month=12, day=31)

    def test_invalid_year_above(self):
        with self.assertRaises(ValueError):
            PESEL().from_date(year=2300, month=1, day=1)

    def test_invalid_month_below(self):
        with self.assertRaises(ValueError):
            PESEL().from_date(year=2016, month=0, day=30)

    def test_invalid_month_above(self):
        with self.assertRaises(ValueError):
            PESEL().from_date(year=2016, month=13, day=30)

    def test_invalid_day_below(self):
        with self.assertRaises(ValueError):
            PESEL().from_date(year=2016, month=11, day=0)

    def test_invalid_day_above(self):
        with self.assertRaises(ValueError):
            PESEL().from_date(year=2016, month=11, day=32)

    def test_leap_year_invalid(self):
        with self.assertRaises(ValueError):
            PESEL().from_date(year=2013, month=2, day=29)

    def test_leap_year_valid(self):
        self.assertTrue(PESEL().from_date(year=2012, month=2, day=29))

    def test_lower_boundary_valid(self):
        self.assertTrue(PESEL().from_date(year=1800, month=1, day=1))

    def test_upper_boundary_valid(self):
        self.assertTrue(PESEL().from_date(year=2299, month=12, day=31))

class TestToString(unittest.TestCase):

    def test_19th_century_one_digit_month(self):
        p = PESEL().from_date(1819, 1, 30)
        p.generate()
        self.assertTrue(p.to_string().startswith("198130"))

    def test_19th_century_two_digit_month(self):
        p = PESEL().from_date(1891, 12, 30)
        p.generate()
        self.assertTrue(p.to_string().startswith("919230"))

    def test_20th_century_one_digit_month(self):
        p = PESEL().from_date(1920, 2, 20)
        p.generate()
        self.assertTrue(p.to_string().startswith("200220"))

    def test_20th_century_two_digit_month(self):
        p = PESEL().from_date(1999, 12, 30)
        p.generate()
        self.assertTrue(p.to_string().startswith("991230"))

    def test_21st_century_one_digit_month(self):
        p = PESEL().from_date(2006, 3, 30)
        p.generate()
        self.assertTrue(p.to_string().startswith("062330"))

    def test_21st_century_two_digit_month(self):
        p = PESEL().from_date(2020, 12, 30)
        p.generate()
        self.assertTrue(p.to_string().startswith("203230"))

    def test_22nd_century_one_digit_month(self):
        p = PESEL().from_date(2111, 4, 30)
        p.generate()
        self.assertTrue(p.to_string().startswith("114430"))

    def test_22nd_century_two_digit_month(self):
        p = PESEL().from_date(2161, 11, 30)
        p.generate()
        self.assertTrue(p.to_string().startswith("615130"))

    def test_23rd_century_one_digit_month(self):
        p = PESEL().from_date(2200, 5, 30)
        p.generate()
        self.assertTrue(p.to_string().startswith("006530"))

    def test_23rd_century_two_digit_month(self):
        p = PESEL().from_date(2299, 12, 29)
        p.generate()
        self.assertTrue(p.to_string().startswith("997229"))

class TestToDate(unittest.TestCase):

    def test_19th_century_one_digit_month(self):
        p = PESEL().from_string("19813012344")
        self.assertEqual( p.to_date("%Y-%m-%d"), "1819-01-30" )

    def test_19th_century_two_digit_month(self):
        p = PESEL().from_string("91923012344")
        self.assertEqual(p.to_date("%Y-%m-%d"), "1891-12-30" )

    def test_20th_century_one_digit_month(self):
        p = PESEL().from_string("20022045678")
        self.assertEqual(p.to_date("%Y-%m-%d"), "1920-02-20" )

    def test_20th_century_two_digit_month(self):
        p = PESEL().from_string("99123085265")
        self.assertEqual(p.to_date("%Y-%m-%d"), "1999-12-30" )

    def test_21st_century_one_digit_month(self):
        p = PESEL().from_string("06233084266")
        self.assertEqual(p.to_date("%Y-%m-%d"), "2006-03-30" )

    def test_21st_century_two_digit_month(self):
        p = PESEL().from_string("20323079310")
        self.assertEqual(p.to_date("%Y-%m-%d"), "2020-12-30" )

    def test_22nd_century_one_digit_month(self):
        p = PESEL().from_string("11443095179")
        self.assertEqual(p.to_date("%Y-%m-%d"), "2111-04-30" )

    def test_22nd_century_two_digit_month(self):
        p = PESEL().from_string("61513035794")
        self.assertEqual(p.to_date("%Y-%m-%d"), "2161-11-30" )

    def test_23rd_century_one_digit_month(self):
        p = PESEL().from_string("00653011554")
        self.assertEqual(p.to_date("%Y-%m-%d"), "2200-05-30" )

    def test_23rd_century_two_digit_month(self):
        p = PESEL().from_string("99722984464")
        self.assertEqual(p.to_date("%Y-%m-%d"), "2299-12-29" )

if __name__ == '__main__':
    unittest.main()
