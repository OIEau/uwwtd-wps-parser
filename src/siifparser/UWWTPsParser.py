from src.siifparser.SiifParserErrorHandler import SiifParserErrorHandler

class UWWTPsParser(SiifParserErrorHandler):

    def __init__(self, db_cursor):
        SiifParserErrorHandler.__init__(self)
        self.c = db_cursor

    def verify_uwwCode(self):
        """
        2. Record uniqueness test
        """
        self.c.execute('''SELECT uwwCode, COUNT(uwwCode) 
                          FROM UWWTPs
                          GROUP BY uwwCode
                          HAVING COUNT(uwwCode) > 1''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False, "The uwwCode '%s' is present %s times", res]
        else:
            return [True]

    def verify_uwwCodeFormat(self):
        """
        2. Record uniqueness test
        """
        self.c.execute('''SELECT a.uwwCode, r.rptMStateKey
                            FROM UWWTPs a , Reporter r
                            WHERE substr(uwwCode, 1, 2) != (SELECT r.rptMStateKey FROM Reporter)
                          ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False, "The uwwCode '%s' does not start with the proper country code '%s' ", res]
        else:
            return [True]

    def verify_uwwLatitudeLongitude(self):
        """
        7.Coordinates test 1
        """
        self.c.execute('''SELECT uwwCode, uwwLatitude, uwwLongitude
                            FROM  UWWTPs 
                            WHERE ( 
                                ((uwwLatitude IS NULL) OR LENGTH(uwwLatitude)=0)
                             OR ((uwwLongitude IS NULL) OR LENGTH(uwwLongitude)=0)
                             OR ((uwwLatitude=0) OR (uwwLongitude=0)))
                             AND uwwState = 1
                        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the UWWTP '%s' with uwwState equal to 1 the uwwLatitude '%s' or uwwLongitude '%s' is empty.",
                    res]
        else:
            return [True]

    def verify_uwwTreatmentType(self):
        """
        9. Type of treatment test - records after deadline
        """
        self.c.execute('''SELECT uwwCode, uwwNRemoval, uwwPRemoval, uwwNTotPerf, uwwPTotPerf, 
                                uwwNRemoval, uwwPRemoval, uwwUV, uwwChlorination, uwwOzonation, 
                                uwwSandFiltration, uwwMicroFiltration
                    FROM (UWWTPs AS u
                          LEFT JOIN Agglomerations AS a ON a.aggCode=u.aggCode)
                          LEFT JOIN ReportPeriod AS rp ON (a.repCode = rp.repCode)
                    WHERE uwwCollectingSystem IN ('ISCON')
                    AND(
                      (     
                                (uwwPrimaryTreatment IS NULL)
                            AND (uwwSecondaryTreatment IS NULL)
                            AND (uwwOtherTreatment IS NULL)
                            AND (uwwNRemoval IS NULL)
                            AND (uwwPRemoval IS NULL)
                            AND (uwwUV IS NULL)
                            AND (uwwChlorination IS NULL)
                            AND (uwwOzonation IS NULL)
                            AND (uwwSandFiltration IS NULL)
                            AND (uwwMicroFiltration IS NULL)
                      ) 
                      OR (
                                (uwwPrimaryTreatment = 0)
                            AND (uwwSecondaryTreatment = 0)
                            AND (uwwOtherTreatment = 0)
                            AND (uwwNRemoval = 0)
                            AND (uwwPRemoval = 0)
                            AND (uwwUV = 0)
                            AND (uwwChlorination = 0)
                            AND (uwwOzonation = 0)
                            AND (uwwSandFiltration = 0)
                            AND (uwwMicroFiltration = 0)
                      )
                    )
                    AND uwwState = 1
                    AND (strftime('%Y', a.aggPeriodOver) <= rp.repReportedPeriod)
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the UWWTP '%s' with uwwState 1 the uwwNRemoval '%s' and uwwPRemoval '%s' and uwwNTotPerf '%s' "
                    "and uwwPTotPerf '%s' and uwwNRemoval '%s' and uwwPRemoval '%s' and uwwUV '%s' and uwwChlorination "
                    "'%s' and uwwOzonation '%s' and uwwSandFiltration  '%s' and  uwwMicroFiltration '%s' are null",
                    res]
        else:
            return [True]

    def verify_treatmentTypeCompletness(self):
        """
        11. Treatment type completness test
        """
        # , uwwCollectingSystem, uwwPrimaryTreatment, uwwSecondaryTreatment, uwwOtherTreatment, uwwNRemoval, uwwPRemoval, uwwUV, uwwChlorination, uwwOzonation, uwwSandFiltration, uwwMicroFiltration
        self.c.execute('''SELECT  uwwCode
                            FROM  UWWTPs
                            WHERE
                            (
                                (uwwSecondaryTreatment = 1 AND (uwwPrimaryTreatment IS NULL OR uwwPrimaryTreatment != 1)) OR
                                (uwwOtherTreatment = 1 AND (uwwSecondaryTreatment IS NULL OR uwwSecondaryTreatment != 1) AND (uwwPrimaryTreatment IS NULL OR uwwPrimaryTreatment != 1)) OR 
                                ( (uwwNRemoval = 1 OR uwwPRemoval = 1) AND  (uwwSecondaryTreatment IS NULL OR uwwSecondaryTreatment != 1) AND  (uwwPrimaryTreatment IS NULL OR uwwPrimaryTreatment != 1) ) OR 
                                ( (uwwUV = 1 OR uwwChlorination = 1 OR uwwOzonation = 1 OR uwwSandFiltration = 1 OR uwwMicroFiltration = 1) AND (uwwSecondaryTreatment IS NULL OR uwwSecondaryTreatment != 1) AND  (uwwPrimaryTreatment IS NULL OR uwwPrimaryTreatment != 1) )
                            )
                            AND uwwState = 1
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the UWWTP '%s' with uwwState 1 there are secondary treatments reported but no primary treatment "
                    "or there are higher level treatemnts reported but no primary or secondary treatment",
                    res]
        else:
            return [True]

    def verify_treatmentPerformance(self):
        """
        12. Treatment performance for N/P completness test
        """
        self.c.execute('''SELECT uwwCode, uwwNTotPerf, uwwNRemoval, uwwPTotPerf, uwwPRemoval 
                            FROM UWWTPs
                            WHERE (
                                (uwwNTotPerf = 'P' AND uwwNRemoval = 'false') OR  
                                (uwwPTotPerf = 'P' AND uwwPRemoval = 'false')
                            )  
                            AND uwwState = 1 
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the UWWTP '%s' with uwwState 1 the uwwNTotPerf is '%s' and uwwNRemoval '%s' OR uwwPTotPerf is '%s' and  uwwNRemoval '%s' ",
                    res]
        else:
            return [True]

    def verify_treatmentEfficiency(self):
        """
        13. Treatment efficiency and performance for N/P consistency test
        """
        self.c.execute('''SELECT  uwwCode 
                            FROM UWWTPs
                            WHERE 
                              (
                                (
                                  uwwPDischargeMeasured IS NOT NULL AND uwwPIncomingMeasured IS NOT NULL AND uwwPIncomingMeasured > 0 
                                  AND 
                                  ( 
                                    (((uwwPIncomingMeasured - uwwPDischargeMeasured) / uwwPIncomingMeasured) >= 0.8 AND uwwPTotPerf <> 'P')
                                    OR
                                    (((uwwPIncomingMeasured - uwwPDischargeMeasured) / uwwPIncomingMeasured) < 0.8 AND uwwPTotPerf <> 'NA')  
                                  )
                                ) OR (
                                  uwwPDischargeCalculated IS NOT NULL AND uwwPIncomingCalculated IS NOT NULL AND uwwPIncomingCalculated > 0 
                                  AND 
                                  ( 
                                    (((uwwPIncomingCalculated - uwwPDischargeCalculated) / uwwPIncomingCalculated) >= 0.8 AND uwwPTotPerf <> 'P')
                                    OR
                                    (((uwwPIncomingCalculated - uwwPDischargeCalculated) / uwwPIncomingCalculated) < 0.8 AND uwwPTotPerf <> 'NA')  
                                  )
                                ) OR (
                                  uwwPDischargeEstimated IS NOT NULL AND uwwPIncomingEstimated IS NOT NULL AND uwwPIncomingEstimated > 0 
                                  AND 
                                  ( 
                                    (((uwwPIncomingEstimated - uwwPDischargeEstimated) / uwwPIncomingEstimated) >= 0.8 AND uwwPTotPerf <> 'P')
                                    OR
                                    (((uwwPIncomingEstimated - uwwPDischargeEstimated) / uwwPIncomingEstimated) < 0.8 AND uwwPTotPerf <> 'NA')  
                                  )
                                ) OR (
                                  uwwNDischargeMeasured IS NOT NULL AND uwwNIncomingMeasured IS NOT NULL AND uwwNIncomingMeasured > 0  
                                  AND 
                                  ( 
                                    (((uwwNIncomingMeasured - uwwNDischargeMeasured) / uwwNIncomingMeasured) >= 0.75 AND uwwPTotPerf <> 'P')
                                    OR
                                    (((uwwNIncomingMeasured - uwwNDischargeMeasured) / uwwNIncomingMeasured) < 0.75 AND uwwPTotPerf <> 'NA')  
                                  )
                                ) OR (
                                  uwwNDischargeCalculated IS NOT NULL AND uwwNIncomingCalculated IS NOT NULL AND uwwNIncomingCalculated > 0   
                                  AND 
                                  ( 
                                    (((uwwNIncomingCalculated - uwwNDischargeCalculated) / uwwNIncomingCalculated) >= 0.75 AND uwwPTotPerf <> 'P')
                                    OR
                                    (((uwwNIncomingCalculated - uwwNDischargeCalculated) / uwwNIncomingCalculated) < 0.75 AND uwwPTotPerf <> 'NA')  
                                  )
                                ) OR (
                                  uwwNDischargeEstimated IS NOT NULL AND uwwNIncomingEstimated IS NOT NULL  AND uwwNIncomingEstimated > 0  
                                  AND 
                                  ( 
                                    (((uwwNIncomingEstimated - uwwNDischargeEstimated) / uwwNIncomingEstimated) >= 0.75 AND uwwPTotPerf <> 'P')
                                    OR
                                    (((uwwNIncomingEstimated - uwwNDischargeEstimated) / uwwNIncomingEstimated) < 0.75 AND uwwPTotPerf <> 'NA')  
                                  )
                                ) 
                              )  
                              AND uwwState = 1
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the UWWTP '%s' with uwwState 1 has inconsistency between reported performance and incoming measures",
                    res]
        else:
            return [True]

    def verify_uwwCapacity(self):
        """
        14. Organic design capacity value presence test
        """
        self.c.execute('''SELECT uwwCode, uwwCapacity
                            FROM UWWTPs
                            WHERE ( uwwCapacity IS NULL OR uwwCapacity=0) AND 
                                  ( uwwCollectingSystem ='ISCON')
                            AND uwwState = 1
                ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the UWWTP '%s' with uwwState 1 and uwwCollectingSystem is ISCON the reported uwwCapacity is '%s'",
                    res]
        else:
            return [True]

    def verify_incomingAndDischargedLoad(self):
        """
        15. Incoming and discharged load values correctness test
        """
        self.c.execute('''SELECT uwwCode FROM UWWTPs
                            WHERE      
                                (             
                                        (uwwBODIncomingMeasured IS NOT NULL AND uwwBODDischargeMeasured IS NOT NULL AND uwwBODIncomingMeasured < uwwBODDischargeMeasured)
                                    OR  (uwwBODIncomingCalculated IS NOT NULL AND uwwBODDischargeCalculated IS NOT NULL AND uwwBODIncomingCalculated < uwwBODDischargeCalculated)
                                    OR  (uwwBODIncomingEstimated IS NOT NULL AND uwwBODDischargeEstimated IS NOT NULL AND uwwBODIncomingEstimated < uwwBODDischargeEstimated)
                                    OR  (uwwCODIncomingMeasured IS NOT NULL AND uwwCODDischargeMeasured IS NOT NULL AND uwwCODIncomingMeasured < uwwCODDischargeMeasured)
                                    OR  (uwwCODIncomingCalculated IS NOT NULL AND uwwCODDischargeCalculated IS NOT NULL AND uwwCODIncomingCalculated < uwwCODDischargeCalculated)
                                    OR  (uwwCODIncomingEstimated IS NOT NULL AND uwwCODDischargeEstimated IS NOT NULL AND uwwCODIncomingEstimated < uwwCODDischargeEstimated)
                                    OR  (uwwNIncomingMeasured IS NOT NULL AND uwwNDischargeMeasured IS NOT NULL AND uwwNIncomingMeasured < uwwNDischargeMeasured)
                                    OR  (uwwNIncomingCalculated IS NOT NULL AND uwwNDischargeCalculated IS NOT NULL AND uwwNIncomingCalculated < uwwNDischargeCalculated)
                                    OR  (uwwNIncomingEstimated IS NOT NULL AND uwwNDischargeEstimated IS NOT NULL AND uwwNIncomingEstimated < uwwNDischargeEstimated)
                                    OR  (uwwPIncomingMeasured IS NOT NULL AND uwwPDischargeMeasured IS NOT NULL AND uwwPIncomingMeasured < uwwPDischargeMeasured)
                                    OR  (uwwPIncomingCalculated IS NOT NULL AND uwwPDischargeCalculated IS NOT NULL AND uwwPIncomingCalculated < uwwPDischargeCalculated)
                                    OR  (uwwPIncomingEstimated IS NOT NULL AND uwwPDischargeEstimated IS NOT NULL AND uwwPIncomingEstimated < uwwPDischargeEstimated)
                                )
                            AND uwwState = 1
                ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the UWWTP '%s' with uwwState 1 the measured discharge load is greater then the incoming load",
                    res]
        else:
            return [True]

    def verify_incomingAndDischargedLoadCompletness(self):
        """
        15. Incoming and discharged load values correctness test
        """
        self.c.execute('''SELECT uwwCode
                            FROM UWWTPs
                            WHERE
                              (
                                (
                                  COALESCE(uwwBODIncomingMeasured, 0) +
                                  COALESCE(uwwBODIncomingCalculated, 0) +
                                  COALESCE(uwwBODIncomingEstimated, 0)
                                ) = 0
                                OR
                                (
                                  COALESCE(uwwBODDischargeMeasured, 0) +
                                  COALESCE(uwwBODDischargeCalculated, 0) +
                                  COALESCE(uwwBODDischargeEstimated, 0)
                                ) = 0
                                OR
                                (
                                  COALESCE(uwwCODIncomingMeasured, 0) +
                                  COALESCE(uwwCODIncomingCalculated, 0) +
                                  COALESCE(uwwCODIncomingEstimated, 0)
                                ) = 0
                                OR
                                (
                                  COALESCE(uwwCODDischargeMeasured, 0) +
                                  COALESCE(uwwCODDischargeCalculated, 0) +
                                  COALESCE(uwwCODDischargeEstimated, 0)
                                ) = 0
                                OR
                                (
                                  COALESCE(uwwNIncomingMeasured, 0) +
                                  COALESCE(uwwNIncomingCalculated, 0) +
                                  COALESCE(uwwNIncomingEstimated, 0)
                                ) = 0
                                OR
                                (
                                  COALESCE(uwwNDischargeMeasured, 0) +
                                  COALESCE(uwwNDischargeCalculated, 0) +
                                  COALESCE(uwwNDischargeEstimated, 0)
                                ) = 0
                                OR
                                (
                                  COALESCE(uwwPIncomingMeasured, 0) +
                                  COALESCE(uwwPIncomingCalculated, 0) +
                                  COALESCE(uwwPIncomingEstimated, 0)
                                ) = 0
                                OR
                                (
                                  COALESCE(uwwPDischargeMeasured, 0) +
                                  COALESCE(uwwPDischargeCalculated, 0) +
                                  COALESCE(uwwPDischargeEstimated, 0)
                                ) = 0
                              )
                              AND uwwState = 1
                              AND uwwCollectingSystem = 'ISCON'
                ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the UWWTP '%s' with uwwState 1 and uwwCollectingSystem ISCON is missing values for discharged or incoming load",
                    res]
        else:
            return [True]


    def verify_potentiallyOverloaded(self):
        """
        18. Potentionally overloaded treatment plants test - records after deadline
        """
        self.c.execute('''SELECT u.uwwCode, a.aggCode
                            FROM (UWWTPs AS u INNER JOIN Agglomerations AS a ON (u.aggCode = a.aggCode AND u.repCode = a.repCode))
                            LEFT JOIN ReportPeriod AS rp ON (a.repCode = rp.repCode)
                            WHERE u.uwwBOD5Perf ='P' OR u.uwwCODPerf='P'
                            AND u.uwwCapacity*1.2 <= u.uwwLoadEnteringUWWTP
                            AND strftime('%Y', a.aggPeriodOver) <= rp.repReportedPeriod
                            AND uwwState = 1
            ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the UWWTP '%s' for the agglomeration '%s' with uwwState 1 and reported has passed is potentially overloaded",
                    res]
        else:
            return [True]

    def verify_allPotentiallyOverloaded(self):
        """
        19. Potentionally overloaded treatment plants test - all records
        """
        self.c.execute('''SELECT uwwCode FROM UWWTPs  
                            WHERE uwwBOD5Perf='P' OR uwwCODPerf='P' AND uwwCapacity*1.2 <= uwwLoadEnteringUWWTP 
                          AND uwwState = 1
        ''')
        res = self.c.fetchall()
        if (len(res) > 0):
            return [False,
                    "In the UWWTP '%s' with uwwState 1 and reported has passed is potentially overloaded",
                    res]
        else:
            return [True]


    # def verify_(self):
    #     """
    #     20. Valid codes test - monitoring results (BOD5, COD) for secondary treatment - records after deadline
    #     """
    #     self.c.execute('''SELECT DISTINCT u.uwwCode, uwwState, uwwCode, uwwBOD5Perf, uwwCODPerf, aggPeriodOver
    #                         FROM UWWTPs AS u
    #                             LEFT JOIN UwwtpAgglos AS ua  ON (u.uwwCode = ua.uwwCode AND u.repCode = ua.repCode)
    #                             LEFT JOIN Agglomerations AS a ON (ua.aggCode = a.aggCode AND ua.repCode = a.repCode)
    #                             LEFT JOIN ReportPeriod AS rp  ON (a.repCode = rp.repCode)
    #                         WHERE (
    #                                                         uwwBOD5Perf IS NULL
    #                                         OR              uwwBOD5Perf <> 'F'
    #                                         OR              uwwBOD5Perf <> 'P'
    #                                         OR              uwwBOD5Perf <> 'NA'
    #                                         OR              uwwBOD5Perf <> 'NR'
    #                                         OR              uwwCODPerf IS NULL
    #                                         OR              uwwCODPerf <> 'F'
    #                                         OR              uwwCODPerf <> 'P'
    #                                         OR              uwwCODPerf <> 'NA'
    #                                         OR              uwwCODPerf <> 'NR' )
    #                             AND             uwwSecondaryTreatment = 1
    #                             AND             uwwCollectingSystem = 'ISCON'
    #                             AND             uwwState = 1
    #                             AND            AND strftime('%Y', a.aggPeriodOver) <= rp.repReportedPeriod
    #     ''')
    #     res = self.c.fetchall()
    #     if (len(res) > 0):
    #         return [False,
    #                 "In the UWWTP '%s' with uwwState 1 and reported has passed is potentially overloaded",
    #                 res]
    #     else:
    #         return [True]


