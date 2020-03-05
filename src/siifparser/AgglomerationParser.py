from src.siifparser.SiifParserErrorHandler import SiifParserErrorHandler


class AgglomerationParser(SiifParserErrorHandler):

    def __init__(self, db_cursor):
        SiifParserErrorHandler.__init__(self)
        self.c = db_cursor

    def verify_aggCode(self):
        """
        2. Record uniqueness test
        """
        self.c.execute('''SELECT aggCode, COUNT(aggCode) 
                          FROM Agglomerations
                          GROUP BY aggCode
                          HAVING COUNT(aggCode) > 1''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False, "The aggCode '%s' is present %s times", res]
        else:
            return [True]

    def verify_aggCodeFormat(self):
        """
        2. Record uniqueness test
        """
        self.c.execute('''SELECT a.aggCode, r.rptMStateKey
                            FROM Agglomerations a , Reporter r
                            WHERE substr(aggCode, 1, 2) != (SELECT r.rptMStateKey FROM Reporter)
                          ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False, "The aggCode '%s' does not start with the proper country code '%s' ", res]
        else:
            return [True]

    def verify_aggBeginLife(self):
        """
        6. Date value tests
        """
        self.c.execute('''SELECT aggCode, aggBeginLife, aggEndLife FROM Agglomerations 
                          WHERE strftime('%Y', aggBeginLife) > strftime('%Y', aggEndLife)''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False, "In the agglomeration '%s' the aggBeginLife '%s' cannot be greater than the aggEndLife '%s'",
                    res]
        else:
            return [True]

    def verify_aggPeriodOver(self):
        """
        6. Date value tests
        """
        self.c.execute('''SELECT aggCode, aggPeriodOver FROM Agglomerations 
                          WHERE aggState = 1 
                          AND (
                            strftime('%Y', aggPeriodOver) < '1998' OR 
                            strftime('%Y', aggPeriodOver) >= '2023'
                          )''')
        res = self.c.fetchall()

        if (len(res) > 0):
            return [False, "In the agglomeration '%s' the aggPeriodOver '%s' has to be comprised between 1998 and 2023",
                    res]
        else:
            return [True]

    def verify_aggDateArt3(self):
        """
        6. Date value tests
        """
        self.c.execute('''SELECT aggCode, aggDateArt3 FROM Agglomerations 
                          WHERE 
                            strftime('%Y-m-d', aggDateArt3 ) < '1998-12-31' OR 
                            strftime('%Y-m-d', aggDateArt3) >= '2030-12-31'
                          ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' the aggDateArt3 '%s' has to be comprised between 1998-12-31 and 2030-12-31",
                    res]
        else:
            return [True]

    def verify_aggDateArt4(self):
        """
        6. Date value tests
        """
        self.c.execute('''SELECT aggCode, aggDateArt4 FROM Agglomerations 
                          WHERE 
                            strftime('%Y-m-d', aggDateArt4 ) < '1998-12-31' OR 
                            strftime('%Y-m-d', aggDateArt4) >= '2030-12-31'
                          ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' the aggDateArt4 '%s' has to be comprised between 1998-12-31 and 2030-12-31",
                    res]
        else:
            return [True]

    def verify_aggDateArt5(self):
        """
        6. Date value tests
        """
        self.c.execute('''SELECT aggCode, aggDateArt5 FROM Agglomerations 
                          WHERE 
                            strftime('%Y-m-d', aggDateArt5 ) < '1998-12-31' OR 
                            strftime('%Y-m-d', aggDateArt5) >= '2030-12-31'
                          ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' the aggDateArt5 '%s' has to be comprised between 1998-12-31 and 2030-12-31",
                    res]
        else:
            return [True]

    def verify_aggDateArt3vsaggDateArt4(self):
        """
        6. Date value tests
        """
        self.c.execute('''SELECT aggCode, aggDateArt3, aggDateArt4 FROM Agglomerations 
                          WHERE strftime('%Y-m-d', aggDateArt3 ) > strftime('%Y-m-d', aggDateArt4)
                       ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' the aggDateArt3 '%s' cannot be greater than aggDateArt4 '%s' ",
                    res]
        else:
            return [True]

    def verify_aggDateArt3vsaggDateArt5(self):
        """
        6. Date value tests
        """
        self.c.execute('''SELECT aggCode, aggDateArt3, aggDateArt5 FROM Agglomerations 
                          WHERE strftime('%Y-m-d', aggDateArt3 ) > strftime('%Y-m-d', aggDateArt5)
                       ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' the aggDateArt3 '%s' cannot be greater than aggDateArt5 '%s' ",
                    res]
        else:
            return [True]

    def verify_aggDateArtvsAggPeriodOver(self):
        """
        6. Date value tests
        """
        self.c.execute('''SELECT aggCode, aggDateArt3, aggDateArt4, aggDateArt5, aggPeriodOver FROM Agglomerations 
                          WHERE  strftime('%Y-m-d', aggDateArt3) > strftime('%Y-m-d', aggPeriodOver)
                          OR     strftime('%Y-m-d', aggDateArt4) > strftime('%Y-m-d', aggPeriodOver) 
                          OR     strftime('%Y-m-d', aggDateArt5) > strftime('%Y-m-d', aggPeriodOver)
                       ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' the aggDateArt3 '%s' or the aggDateArt4 '%s' or the aggDateArt5 '%s' cannot be greater than the aggPeriodOver '%s' ",
                    res]
        else:
            return [True]

    def verify_aggWasterwaterPathway(self):
        """
        7. Wastewater pathway test
        """
        self.c.execute('''SELECT aggCode, (aggC1+aggC2+aggPercWithoutTreatment)
                            FROM Agglomerations
                            WHERE (aggC1 + aggC2 + aggPercWithoutTreatment) != 100  
                            AND aggState=1
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' aggC1 + aggC2 + aggPercWithoutTreatment is equal to must be equal '%s' instead of 100%%",
                    res]
        else:
            return [True]

    def verify_aggLatitudeLongitude(self):
        """
        8.Coordinates test 1
        """
        self.c.execute('''SELECT aggCode, aggLatitude, aggLongitude
                            FROM  Agglomerations 
                            WHERE ( 
                                ((aggLatitude IS NULL) OR LENGTH(aggLatitude)=0)
                             OR ((aggLongitude IS NULL) OR LENGTH(aggLongitude)=0)
                             OR ((aggLatitude=0) OR (aggLongitude=0)))
                             AND aggState = 1
                        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' with aggState equal to 1 the aggLatitude '%s' or aggLongitude '%s' is empty.",
                    res]
        else:
            return [True]

    def verify_aggName(self):
        """
        10. Names test
        """
        self.c.execute(''' SELECT aggCode, aggName
                            FROM Agglomerations
                            WHERE aggName IS NULL OR aggName = ''
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' the aggName '%s' is empty.",
                    res]
        else:
            return [True]

    def verify_aggGenerated(self):
        """
        11. Generated load test
        """

        self.c.execute('''SELECT aggCode, aggPeriodOver, rp.repReportedPeriod, aggGenerated 
                            FROM Agglomerations AS ag
                            LEFT JOIN ReportPeriod AS rp ON (ag.repCode = rp.repCode)
                            WHERE (aggState = 1)
                            AND ((aggGenerated IS NULL) OR (aggGenerated=0))
                            AND ((strftime('%Y', aggPeriodOver)) <= rp.repReportedPeriod)
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' that has the aggState equal to 1 and for which the implementation "
                    "deadline '%s' is expired (reported year is '%s') has no generated load reported (aggGenerated='%s')",
                    res]
        else:
            return [True]

    def verify_aggC1(self):
        """
        12. Wastewater pathway through collecting system test
        """
        self.c.execute('''SELECT aggCode, aggC1
                          FROM Agglomerations
                          WHERE aggState = 1  AND ((aggC1) IS NULL OR (aggC1)>100 OR (aggC1)<0)
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' that has the aggState equal to 1 the reported aggC1 '%s' is incorrect",
                    res]
        else:
            return [True]

    def verify_aggC2(self):
        """
        13. Wastewater pathway addressed through IAS test
        """
        self.c.execute('''SELECT aggCode, aggC2  
                            FROM Agglomerations
                            WHERE (aggState = 1) AND ((aggC2) IS NULL OR (aggC2)>100 OR (aggC2)<0)
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' that has the aggState equal to 1 the reported aggC2 '%s' is incorrect",
                    res]
        else:
            return [True]

    def verify_aggCalculation(self):
        """
        18. Agglomeration Calculation information presence test
        """
        self.c.execute('''SELECT aggCode
                            FROM Agglomerations
                            WHERE aggCalculation IS NULL OR aggCalculation = ""
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "The agglomeration '%s' has no aggCalcultation reported",
                    res]
        else:
            return [True]

    def verify_aggPercPrimTreatment(self):
        """
        19. Generated load addressed via IAS- primary treatment information presence test
        """
        self.c.execute('''SELECT aggCode, (aggC2*aggGenerated/100)
                            FROM Agglomerations
                            WHERE (aggC2*aggGenerated/100) >= 2000 
                            AND aggPercPrimTreatment IS NULL OR aggPercPrimTreatment = ""
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' aggPercPrimTreatment must be reported since the generated load is '%s'",
                    res]
        else:
            return [True]

    def verify_aggPercSecTreatment(self):
        """
        20. Generated load addressed via IAS / secondary treatment information presence test
        """
        self.c.execute('''SELECT aggCode, (aggC2*aggGenerated/100)
                            FROM Agglomerations
                            WHERE (aggC2*aggGenerated/100  >= 2000)
                            AND aggPercSecTreatment IS NULL OR aggPercSecTreatment = ""  
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' aggPercSecTreatment must be reported since the generated load is '%s'",
                    res]
        else:
            return [True]

    def verify_aggPercStringentTreatment(self):
        """
        21. Generated load addressed via IAS /more stringent treatment information presence test
        """
        self.c.execute('''SELECT aggCode, (aggC2*aggGenerated/100)
                            FROM Agglomerations
                            WHERE (aggC2*aggGenerated/100  >= 2000)
                            AND aggPercStringentTreatment IS NULL OR aggPercStringentTreatment = ""  
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' aggPercStringentTreatment must be reported since the generated load is '%s'",
                    res]
        else:
            return [True]

    def verify_aggPeriodOverEU15(self):
        """
        22. Period over for EU15 value test
        """
        self.c.execute('''SELECT aggCode, aggPeriodOver
                             FROM Agglomerations
                             WHERE
                                (
                                    substr(aggCode, 1, 2) = 'AT' OR
                                    substr(aggCode, 1, 2) = 'BE' OR
                                    substr(aggCode, 1, 2) = 'DK' OR
                                    substr(aggCode, 1, 2) = 'FI' OR
                                    substr(aggCode, 1, 2) = 'FR' OR
                                    substr(aggCode, 1, 2) = 'DE' OR
                                    substr(aggCode, 1, 2) = 'GR' OR
                                    substr(aggCode, 1, 2) = 'IE' OR
                                    substr(aggCode, 1, 2) = 'IT' OR
                                    substr(aggCode, 1, 2) = 'LU' OR
                                    substr(aggCode, 1, 2) = 'NL' OR
                                    substr(aggCode, 1, 2) = 'PT' OR
                                    substr(aggCode, 1, 2) = 'ES' OR
                                    substr(aggCode, 1, 2) = 'SE' OR
                                    substr(aggCode, 1, 2) = 'UK'
                                )
                                AND (
                                    aggPeriodOver IS NULL
                                    OR  strftime('%Y', aggPeriodOver) > '2005'
                                    OR  strftime('%Y', aggPeriodOver) < '1998'
                                )
                             AND aggState = 1
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' the aggPeriodOver of '%s' must be between 1998 and 2005 for EU15 member states",
                    res]
        else:
            return [True]

    def verify_aggPeriodOverEU12(self):
        """
        22. Period over for EU15 value test
        """
        self.c.execute('''SELECT aggCode, aggPeriodOver
                             FROM Agglomerations
                             WHERE
                                (
                                    (substr(aggCode, 1, 2) = 'CY' AND strftime('%Y-%m-%d', aggPeriodOver) > '2012-12-31') OR
                                    (substr(aggCode, 1, 2) = 'CZ' AND strftime('%Y-%m-%d', aggPeriodOver) > '2010-12-31') OR
                                    (substr(aggCode, 1, 2) = 'EE' AND strftime('%Y-%m-%d', aggPeriodOver) > '2010-12-31') OR
                                    (substr(aggCode, 1, 2) = 'LV' AND strftime('%Y-%m-%d', aggPeriodOver) > '2015-12-31') OR
                                    (substr(aggCode, 1, 2) = 'LI' AND strftime('%Y-%m-%d', aggPeriodOver) > '2009-12-31') OR
                                    (substr(aggCode, 1, 2) = 'HU' AND strftime('%Y-%m-%d', aggPeriodOver) > '2015-12-31') OR
                                    (substr(aggCode, 1, 2) = 'MT' AND strftime('%Y-%m-%d', aggPeriodOver) > '2006-12-31') OR
                                    (substr(aggCode, 1, 2) = 'PO' AND strftime('%Y-%m-%d', aggPeriodOver) > '2015-12-31') OR
                                    (substr(aggCode, 1, 2) = 'SI' AND strftime('%Y-%m-%d', aggPeriodOver) > '2015-12-31') OR
                                    (substr(aggCode, 1, 2) = 'SK' AND strftime('%Y-%m-%d', aggPeriodOver) > '2015-12-31') OR
                                    (substr(aggCode, 1, 2) = 'BG' AND strftime('%Y-%m-%d', aggPeriodOver) > '2014-12-31') OR
                                    (substr(aggCode, 1, 2) = 'RO' AND strftime('%Y-%m-%d', aggPeriodOver) > '2018-12-31') OR
                                    (substr(aggCode, 1, 2) = 'HR' AND strftime('%Y-%m-%d', aggPeriodOver) > '2023-12-31') 
                                )
                             AND aggState = 1
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the agglomeration '%s' the aggPeriodOver of '%s' must be between 1998 and 2005 for EU12 member states",
                    res]
        else:
            return [True]
