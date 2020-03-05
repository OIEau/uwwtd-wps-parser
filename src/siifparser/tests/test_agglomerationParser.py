from unittest import TestCase
from src.siifparser.AgglomerationParser import AgglomerationParser
import sqlite3


class TestAgglomerationParser(TestCase):
    conn = sqlite3.connect('test_siifparser.db')
    c = conn.cursor()
    agg_parser = AgglomerationParser(c)

    def test_run_all_tests(self):
        self.agg_parser.run_all_tests()
        self.agg_parser.print_errors()

    def test_verify_aggCode(self):
        test = self.agg_parser.verify_aggCode()
        self.assertFalse(test[0])

    def test_verify_aggBeginLife(self):
        test = self.agg_parser.verify_aggBeginLife()
        self.assertFalse(test[0])

    def test_verify_aggPeriodOver(self):
        test = self.agg_parser.verify_aggPeriodOver()
        self.assertFalse(test[0])

    def test_verify_aggDateArt3(self):
        test = self.agg_parser.verify_aggDateArt3()
        self.assertFalse(test[0])

    def test_verify_aggDateArt4(self):
        test = self.agg_parser.verify_aggDateArt4()
        self.assertFalse(test[0])

    def test_verify_aggDateArt5(self):
        test = self.agg_parser.verify_aggDateArt5()
        self.assertFalse(test[0])

    def test_verify_aggDateArt3vsaggDateArt4(self):
        test = self.agg_parser.verify_aggDateArt3vsaggDateArt4()
        self.assertFalse(test[0])

    def test_verify_aggDateArt3vsaggDateArt5(self):
        test = self.agg_parser.verify_aggDateArt3vsaggDateArt5()
        self.assertFalse(test[0])

    def test_verify_aggCodeFormat(self):
        test = self.agg_parser.verify_aggDateArt3vsaggDateArt5()
        self.assertFalse(test[0])

    def test_verify_aggWasterwaterPathway(self):
        test = self.agg_parser.verify_aggWasterwaterPathway()
        self.assertFalse(test[0])

    def test_verify_aggLatitudeLongitude(self):
        test = self.agg_parser.verify_aggLatitudeLongitude()
        self.assertFalse(test[0])

    def test_verify_aggName(self):
        test = self.agg_parser.verify_aggName()
        self.assertFalse(test[0])

    def test_verify_aggGenerated(self):
        test = self.agg_parser.verify_aggGenerated()
        self.assertFalse(test[0])

    def test_verify_aggC1(self):
        test = self.agg_parser.verify_aggC1()
        self.assertFalse(test[0])

    def test_verify_aggC2(self):
        test = self.agg_parser.verify_aggC2()
        self.assertFalse(test[0])

    def test_verify_aggCalculation(self):
        test = self.agg_parser.verify_aggCalculation()
        self.assertFalse(test[0])

    def test_verify_aggPercPrimTreatment(self):
        test = self.agg_parser.verify_aggPercPrimTreatment()
        self.assertFalse(test[0])

    def test_verify_aggPercSecTreatment(self):
        test = self.agg_parser.verify_aggPercSecTreatment()
        self.assertFalse(test[0])

    def test_verify_aggPercStringentTreatment(self):
        test = self.agg_parser.verify_aggPercStringentTreatment()
        self.assertFalse(test[0])

    def test_verify_aggPeriodOverEU15(self):
        test = self.agg_parser.verify_aggPeriodOverEU15()
        self.assertFalse(test[0])

    def test_verify_aggPeriodOverEU12(self):
        test = self.agg_parser.verify_aggPeriodOverEU12()
        self.assertFalse(test[0])

