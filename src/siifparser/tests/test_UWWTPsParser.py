from unittest import TestCase
from src.siifparser.UWWTPsParser import UWWTPsParser
import sqlite3


class TestUWWTPsParser(TestCase):
    conn = sqlite3.connect('test_siifparser.db')
    c = conn.cursor()
    agg_parser = UWWTPsParser(c)

    def test_run_all_tests(self):
        self.agg_parser.run_all_tests()
        self.agg_parser.print_errors()

    def test_verify_uwwCode(self):
        test = self.agg_parser.verify_uwwCode()
        self.assertFalse(test[0])

    def test_verify_uwwCodeFormat(self):
        test = self.agg_parser.verify_uwwCodeFormat()
        self.assertFalse(test[0])

    def test_verify_uwwLatitudeLongitude(self):
        test = self.agg_parser.verify_uwwLatitudeLongitude()
        self.assertFalse(test[0])

    def test_verify_uwwTreatmentType(self):
        test = self.agg_parser.verify_uwwTreatmentType()
        self.assertFalse(test[0])

    def test_verify_treatmentTypeCompletness(self):
        test = self.agg_parser.verify_treatmentTypeCompletness()
        self.assertFalse(test[0])

    def test_verify_treatmentPerformance(self):
        test = self.agg_parser.verify_treatmentPerformance()
        self.assertFalse(test[0])

    def test_verify_treatmentEfficiency(self):
        test = self.agg_parser.verify_treatmentEfficiency()
        self.assertFalse(test[0])

    def test_verify_uwwCapacity(self):
        test = self.agg_parser.verify_uwwCapacity()
        self.assertFalse(test[0])

    def test_verify_incomingAndDischargedLoad(self):
        test = self.agg_parser.verify_incomingAndDischargedLoad()
        self.assertFalse(test[0])

    def test_verify_incomingAndDischargedLoadCompletness(self):
        test = self.agg_parser.verify_incomingAndDischargedLoadCompletness()
        self.assertFalse(test[0])

    def test_verify_potentiallyOverloaded(self):
        test = self.agg_parser.verify_potentiallyOverloaded()
        self.assertFalse(test[0])

    def test_verify_allPotentiallyOverloaded(self):
        test = self.agg_parser.verify_allPotentiallyOverloaded()
        self.assertFalse(test[0])