from pywps import Process, LiteralInput, ComplexInput, LiteralOutput, UOM, Format
from pywps.validator.mode import MODE
from lxml import etree

from src.siifparser.SiifParser import SiifParser


class UWWTDParser(Process):
    def __init__(self):
        inputs = ComplexInput(
            'uwwtd_data',
            'UWWTD reporting data',
            supported_formats=[Format('application/xml')],
            mode=MODE.NONE
        )

        inputs = [inputs]
        outputs = [LiteralOutput('response',
                                 'Output response', data_type='string')]

        super(UWWTDParser, self).__init__(
            self._handler,
            identifier='UWWTDParser',
            title='Process UWWTDParser',
            abstract='UWWTDParser',
            version='1.0.0',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        parser = SiifParser(xml_string=request.inputs['uwwtd_data'][0].file)
        parser.validate_xsd()
        parser.init_db()
        parser.fill_db_from_xml()
        parser.verify_db()
        errors_string = parser.get_xsd_errors_as_string()
        errors_string += parser.get_db_errors_as_string()
        response.outputs['response'].data = errors_string
        return response
