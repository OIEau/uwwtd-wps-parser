import os
from lxml import etree
from io import StringIO


class XSDValidator:

    xsd = os.getcwd() + 'data/schemas/schema-dst-3381.xsd'
    xml = os.getcwd()
    feedErrors = 0
    errorDetails = ''

    def __init__(self, xsd, xml):
        if (os.path.isfile(xsd)):
            self.xsd= xsd
        if (os.path.isfile(xml)):
            self.xml = xml

    def validate(self):
        try:
            with open(self.xsd, 'r') as schema_file:
                schema_to_check = schema_file.read()

            with open(self.xml, 'r') as xml_file:
                xml_to_check = xml_file.read()

            xmlschema_doc = etree.parse(StringIO(schema_to_check))
            xmlschema = etree.XMLSchema(xmlschema_doc)

            doc = etree.parse(StringIO(xml_to_check))
            print('XML well formed, syntax ok.')

            # validate against schema
            xmlschema.assertValid(doc)
            print('XML valid, schema validation ok.')

        # check for file IO error
        except IOError:
            print('Invalid File')

        # check for XML syntax errors
        except etree.XMLSyntaxError as err:
            print(vars(err))
            print(str(err.error_log))

        except etree.DocumentInvalid as err:
            # print('Schema validation error, see error_schema.log')
            # with open('error_schema.log', 'w') as error_log_file:
            #    error_log_file.write(str(err.error_log))
            print(vars(err))
            print(str(err.error_log))

        quit()
