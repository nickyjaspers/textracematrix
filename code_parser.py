
class CodeParser:
    def __init__(self, req_pattern='// REQ:', test_pattern='@Test', method_pattern='public void '):
        self.req_test_mapping = dict()
        self.req_pattern = req_pattern
        self.test_pattern = test_pattern
        self.method_pattern = method_pattern

    def get_requirements_and_test_cases(self, file_to_parse):
        requirements = None
        criteria_requirement = False
        criteria_test = False
        criteria_method_name = False
        with open(file_to_parse) as f:
            lines = f.readlines()
            for line in lines:
                # find requirements
                if not criteria_requirement:
                    requirements = self.get_requirements_from_requirements_line(line)
                    if len(requirements) > 0:
                        criteria_requirement = True

                # find test
                if criteria_requirement is True and criteria_test is False:
                    if self.is_test(line):
                        criteria_test = True

                # find method name
                if criteria_requirement is True and criteria_test is True and criteria_method_name is False:
                    method_name = self.get_method_name(line)
                    if method_name:
                        # check if al criteria met, add entry in mapping, and reset al criteria
                        self.req_test_mapping[method_name] = requirements
                        criteria_requirement = False
                        criteria_test = False

    def get_requirements_from_requirements_line(self, line):
        requirements = []
        if self.req_pattern not in line:
            return requirements

        s = line.strip().lstrip(self.req_pattern)
        for req in s.split(","):
            requirements.append(req.strip())
        return requirements

    def is_test(self, line):
        if self.test_pattern in line.strip():
            return True
        return False

    def get_method_name(self, line):
        if self.method_pattern not in line:
            return False

        s = line.strip().lstrip(self.method_pattern).split('(')
        return s[0]