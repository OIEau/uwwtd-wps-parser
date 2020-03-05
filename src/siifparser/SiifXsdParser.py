from lxml import etree
from src.siifparser.SiifParserErrorHandler import SiifParserErrorHandler


class SiifXsdParser(SiifParserErrorHandler):

    def __init__(self):
        SiifParserErrorHandler.__init__(self)

    def validate_xsd(self, xmltree, xsd_file='src/siifparser/data/schemas/schema-dst-3381.xsd'):
        try:
            # validate against schema
            parser = etree.XMLParser(remove_comments=True)
            xsdtree = etree.parse(xsd_file, parser=parser)
            xsd = etree.XMLSchema(xsdtree)
            xsd.assertValid(xmltree)
            self.error_log['verify_XMLSyntax'] = [True, ""]
            self.error_log['verify_DocumentXML'] = [True, ""]

        except etree.DocumentInvalid as err:
            errstr = ""
            for error in err.error_log:
                errstr += "\t\tLine %s Column %s: %s\n" % (str(error.line), str(error.column), str(error.message))
            self.error_log['verify_DocumentXML'] = [False, errstr]

        # # check for XML syntax errors
        # except etree.XMLSyntaxError as err:
        #     self.error_log['verify_XMLSyntax'] = [False, str(err.error_log)]
