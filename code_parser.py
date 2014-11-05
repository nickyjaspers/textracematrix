
class CodeParser:
    def __init__(self):
        self.req_test_mapping = dict()

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

    @staticmethod
    def get_requirements_from_requirements_line(line, pattern='// REQ:'):
        requirements = []
        if pattern not in line:
            return requirements

        s = line.strip().lstrip(pattern)
        for req in s.split(","):
            requirements.append(req.strip())
        return requirements

    @staticmethod
    def is_test(line, pattern='@Test'):
        if pattern in line.strip():
            return True
        return False

    @staticmethod
    def get_method_name(line, pattern='public void '):
        if pattern not in line:
            return False

        s = line.strip().lstrip(pattern).split('(')
        return s[0]