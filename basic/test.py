#!/usr/bin/env python
# -*- coding: utf-8 -*-

print "******start******"

def get_city_country(city, county):
	return city.title() + ', ' + county.title()

import unittest

class CityCountryTest(unittest.TestCase):
	def test_get_city_country(self):
		s = get_city_country('santiago', 'Chile')
		self.assertEqual(s, 'Santiago, Chile')

unittest.main()