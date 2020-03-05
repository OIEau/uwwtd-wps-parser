from collections import OrderedDict
import configparser
import re
import pprint

class SiifParserErrorHandler:

    def __init__(self, error_levels_file="src/siifparser/error_levels.conf"):
        self.error_log = OrderedDict()
        self.levels_config = configparser.ConfigParser()
        self.levels_config.read(error_levels_file)

    def run_all_tests(self):
        for attr in dir(self):
            if re.match("verify_.*", attr):
                test_result = getattr(self, attr)()
                self.error_log[attr] = test_result

    def get_errors(self):
        return self.error_log

    def print_errors(self):
        print(self.get_errors_as_string())

    def get_errors_as_string(self):
        err_ret = "\n"
        for test_name, results in self.error_log.items():
            err_ret += "=== running test '"+test_name+"' ===\n"
            if (results[0] is False):
                err_ret += "\t"+self.levels_config[self.__class__.__name__][test_name].upper()+"\n"
                if len(results) >= 3:
                    for result in results[2]:
                        err_ret += "\t\t" + results[1] % result + "\n"
                else :
                    err_ret += results[1]
            else:
                err_ret += "\tPASSED\n"
            err_ret += "\n"
        return err_ret