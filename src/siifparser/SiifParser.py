import sqlite3
from lxml import etree
from collections import OrderedDict
from src.siifparser.AgglomerationParser import AgglomerationParser
from src.siifparser.UWWTPsParser import UWWTPsParser
from src.siifparser.SiifXsdParser import SiifXsdParser

class SiifParser:
    def __init__(self, xml_file='', xml_string='', error_levels_file='error_levels.conf', db_file='workdir/siifparser.db'):
        # init xml
        if xml_file != "":
            self.xmlsource = xml_file
        if xml_string != "":
            self.xmlsource = xml_string

        # init sqlite db
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        # init db parser obj
        self.agglomeration_parser = AgglomerationParser(self.c)
        self.uwwtps_parser = UWWTPsParser(self.c)
        self.xsd_parser = SiifXsdParser()

    def validate_xsd(self):
        parser = etree.XMLParser(remove_comments=True)
        self.xmltree = etree.parse(self.xmlsource, parser=parser)
        self.xsd_parser.validate_xsd(self.xmltree)


    def init_db(self):
        self.c.execute('''DROP TABLE IF EXISTS Reporter''')
        self.c.execute('''CREATE TABLE Reporter
                        (   rptMStateKey text,
                            rptMStateValue text,
                            rptCulture text 
                        )
        ''')
        self.c.execute('''DROP TABLE IF EXISTS ReportPeriod''')
        self.c.execute('''CREATE TABLE ReportPeriod
                        (   rptMStateKey text,
                            repCode text,
                            repVersion text,
                            repSituationAt text,
                            repReportedPeriod text,
                            repReferenceSystem text
                        )
        ''')
        self.c.execute('''DROP TABLE IF EXISTS Agglomerations''')
        self.c.execute('''CREATE TABLE Agglomerations
                     (  aggState integer,
                        repCode text,
                        aggCode text,
                        aggName text,
                        aggNUTS text,
                        aggLatitude real,
                        aggLongitude real,
                        aggGenerated integer,
                        bigCityID text,
                        aggCalculation text,
                        aggChanges text,
                        aggChangesComment text,
                        aggPeriodOver text,
                        aggDateArt3 text,
                        aggDateArt4 text,
                        aggDateArt5 text,
                        aggC1 integer,
                        aggMethodC1 text,
                        aggC2 integer,
                        aggMethodC2 text,
                        aggPercWithoutTreatment real,
                        aggMethodWithoutTreatment text,
                        aggPercPrimTreatment real,
                        aggPercSecTreatment real,
                        aggPercStringentTreatment real,
                        aggHaveRegistrationSystem text,
                        aggExistMaintenancePlan text,
                        aggPressureTest text,
                        aggVideoInspections text,
                        aggOtherMeasures text,
                        aggExplanationOther text,
                        aggSewageNetwork text,
                        aggBestTechnicalKnowledge text,
                        aggDilutionRates text,
                        aggCapacity text,
                        aggAccOverflows text,
                        aggAccOverflowNumber integer,
                        aggSewerOverflows_m3 integer,
                        aggSewerOverflows_pe integer,
                        aggForecast text,
                        aggBeginLife text,
                        aggEndLife text,
                        aggHyperlink text,
                        aggRemarks text
                     )''')
        self.c.execute('''DROP TABLE IF EXISTS UWWTPs''')
        self.c.execute('''CREATE TABLE UWWTPs
                     (  uwwState integer,
                        repCode text,
                        aggCode text,
                        uwwCode text,
                        uwwName text,
                        uwwCollectingSystem text,
                        uwwDateClosing numeric,
                        uwwHistorie text,
                        uwwLatitude real,
                        uwwLongitude real,
                        uwwNUTS interger,
                        uwwLoadEnteringUWWTP interger,
                        uwwCapacity integer,
                        uwwPrimaryTreatment text,
                        uwwSecondaryTreatment text,
                        uwwOtherTreatment text,
                        uwwNRemoval text,
                        uwwPRemoval text,
                        uwwUV text,
                        uwwChlorination text,
                        uwwOzonation text,
                        uwwSandFiltration text,
                        uwwMicroFiltration text,
                        uwwOther text,
                        uwwSpecification text,
                        uwwBOD5Perf text,
                        uwwCODPerf text,
                        uwwTSSPerf text,
                        uwwNTotPerf text,
                        uwwPTotPerf text,
                        uwwOtherPerf text,
                        uwwBadPerformance text,
                        uwwAccidents text,
                        uwwBadDesign text,
                        uwwInformation text,
                        uwwBODIncomingMeasured real,
                        uwwBODIncomingCalculated real,
                        uwwBODIncomingEstimated real,
                        uwwCODIncomingMeasured real,
                        uwwCODIncomingCalculated real,
                        uwwCODIncomingEstimated real,
                        uwwNIncomingMeasured real,
                        uwwNIncomingCalculated real,
                        uwwNIncomingEstimated real,
                        uwwPIncomingMeasured real,
                        uwwPIncomingCalculated real,
                        uwwPIncomingEstimated real,
                        uwwBODDischargeMeasured real,
                        uwwBODDischargeCalculated real,
                        uwwBODDischargeEstimated real,
                        uwwCODDischargeMeasured real,
                        uwwCODDischargeCalculated real,
                        uwwCODDischargeEstimated real,
                        uwwNDischargeMeasured real,
                        uwwNDischargeCalculated real,
                        uwwNDischargeEstimated real,
                        uwwPDischargeMeasured real,
                        uwwPDischargeCalculated real,
                        uwwPDischargeEstimated real,
                        uwwWasteWaterTreated real,
                        uwwMethodWasteWaterTreated text,
                        uwwBeginLife numeric,
                        uwwEndLife numeric,
                        uwwHyperlink text,
                        uwwRemarks text
                     )''')

        self.c.execute('''DROP TABLE IF EXISTS DischargePoints''')
        self.c.execute('''CREATE TABLE DischargePoints
                    (   dcpState text,
                        repCode text,
                        uwwCode text,
                        dcpCode text,
                        dcpName text,
                        dcpNUTS text,
                        dcpLatitude real,
                        dcpLongitude real,
                        dcpWaterBodyType text,
                        dcpIrrigation text,
                        dcpTypeOfReceivingArea text,
                        rcaCode string,
                        dcpSurfaceWaters text,
                        dcpWaterbodyID text,
                        dcpNotAffect text,
                        dcpMSProvide text,
                        dcpCOMAccept text,
                        dcpGroundWater text,
                        dcpReceivingWater text,
                        dcpWFDSubUnit text,
                        dcpWFDRBD text,
                        dcpWaterBodyReferenceDate text,
                        dcpGroundWaterReferenceDate text,
                        dcpReceivingWaterReferenceDate text,
                        dcpWFDSubUnitReferenceDate text,
                        dcpWFDRBDReferenceDate text,
                        dcpBeginLife text,
                        dcpEndLife text,
                        dcpRemarks text
                    )''')

    def fill_db_from_xml(self):
        namespaces = {'u': 'http://dd.eionet.europa.eu/namespaces/802',
                      'rp': 'http://dd.eionet.europa.eu/namespaces/817',
                      'r': 'http://dd.eionet.europa.eu/namespaces/816',
                      'a': 'http://dd.eionet.europa.eu/namespaces/820',
                      't': 'http://dd.eionet.europa.eu/namespaces/821',
                      'd': 'http://dd.eionet.europa.eu/namespaces/823'}

        # foreach reporter
        reporters = self.xmltree.xpath('/u:UWWTDArt15/r:Reporter/r:Row', namespaces=namespaces)
        for index, reporter in enumerate(reporters):
            field_names = ""
            field_values = ""
            for elem in reporter:
                if(elem.text != None):
                    if field_names != "":
                        field_names += ","
                    if field_values != "":
                        field_values += ","
                    field_names += etree.QName(elem).localname
                    field_values += '"' + elem.text.replace('"', '""') + '"'
            self.c.execute("""INSERT INTO Reporter (""" + field_names + """) VALUES (""" + field_values + """)""")
        self.conn.commit()

        # foreach ReportPeriod
        reportPeriods = self.xmltree.xpath('/u:UWWTDArt15/rp:ReportPeriod/rp:Row', namespaces=namespaces)
        for index, reportPeriod in enumerate(reportPeriods):
            field_names = ""
            field_values = ""
            for elem in reportPeriod:
                if(elem.text != None):
                    if field_names != "":
                        field_names += ","
                    if field_values != "":
                        field_values += ","
                    field_names += etree.QName(elem).localname
                    field_values += '"' + elem.text.replace('"', '""') + '"'
            self.c.execute("""INSERT INTO ReportPeriod(""" + field_names + """) VALUES (""" + field_values + """)""")
        self.conn.commit()

        # foreach agglo
        agglomerations = self.xmltree.xpath('/u:UWWTDArt15/a:Agglomerations/a:Row', namespaces=namespaces)
        for index, agglo in enumerate(agglomerations):
            field_names = ""
            field_values = ""
            for elem in agglo:
                if(elem.text != None):
                    if field_names != "":
                        field_names += ","
                    if field_values != "":
                        field_values += ","
                    field_names += etree.QName(elem).localname
                    field_values += '"' + elem.text.replace('"', '""') + '"'
            self.c.execute("""INSERT INTO Agglomerations (""" + field_names + """) VALUES (""" + field_values + """)""")
        self.conn.commit()

        # foreach uwwtp
        uwwtps = self.xmltree.xpath('/u:UWWTDArt15/t:UWWTPs/t:Row', namespaces=namespaces)
        for index, uwwtp in enumerate(uwwtps):
            field_names = ""
            field_values = ""
            for elem in uwwtp:
                if(elem.text != None):
                    if field_names != "":
                        field_names += ","
                    if field_values != "":
                        field_values += ","
                    field_names += etree.QName(elem).localname
                    field_values += '"' + elem.text.replace('"', '""') + '"'
            self.c.execute("""INSERT INTO UWWTPs (""" + field_names + """) VALUES (""" + field_values + """)""")
        self.conn.commit()

        # foreach DischargePoints
        DischargePoints = self.xmltree.xpath('/u:UWWTDArt15/d:DischargePoints/d:Row', namespaces=namespaces)
        for index, uwwtp in enumerate(DischargePoints):
            field_names = ""
            field_values = ""
            for elem in uwwtp:
                if(elem.text != None):
                    if field_names != "":
                        field_names += ","
                    if field_values != "":
                        field_values += ","
                    field_names += etree.QName(elem).localname
                    field_values += '"' + elem.text.replace('"', '""') + '"'
            self.c.execute("""INSERT INTO DischargePoints (""" + field_names + """) VALUES (""" + field_values + """)""")
        self.conn.commit()

    def verify_db(self):
        self.agglomeration_parser.run_all_tests()
        self.uwwtps_parser.run_all_tests()

    def get_xsd_errors_as_string(self):
        return self.xsd_parser.get_errors_as_string()

    def print_xsd_errors(self):
       self.xsd_parser.print_errors()

    def get_db_errors_as_string(self):
        errors  = self.agglomeration_parser.get_errors_as_string()
        errors += self.uwwtps_parser.get_errors_as_string()
        return errors

    def print_db_errors(self):
        print(self.agglomeration_parser.get_errors_as_string())
        print(self.uwwtps_parser.get_errors_as_string())
