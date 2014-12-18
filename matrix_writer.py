from math import ceil


class MatrixWriter:
    def __init__(self, req_tests_mapping):
        self.req_tests_mapping = req_tests_mapping
        self.requirements = self.get_requirements_set()

    def get_requirements_set(self):
        self.requirements = set()

        for key in self.req_tests_mapping:
            for req in self.req_tests_mapping[key]:
                self.requirements.add(req)

        return sorted(self.requirements)

    def get_tests_for_requirement(self, requirement):
        tests = list()
        for key in self.req_tests_mapping:
            if requirement in self.req_tests_mapping[key]:
                tests.append(key)

        return sorted(tests)

    def get_result_for_test(self, test):
        pass

    def write_table_header(self, filename, columns):
        # begin longtable definition
        filename.write('\\begin{longtable}[l]{')
        for c in range(0, columns + 1):
            filename.write('|c')
        filename.write('|}\n')

        #write caption
        filename.write('\\caption{Requirements traceability matrix}\\\\ \n')
        filename.write('\\hline \n')

    def write_table_header_requirements(self, filename, columns, range_start):
        filename.write('\\textbf{Req. ID} & ')
        cnt = 0;
        for req in self.requirements[range_start:(range_start + columns)]:
            cnt += 1
            filename.write('\\textbf{')
            filename.write(req)
            filename.write('}')
            if cnt < len(self.requirements[range_start:(range_start + columns)]):
                filename.write(' & ')
        filename.write("\\\\ \n")
        filename.write('\\hline \n')
        filename.write('\\endfirsthead \n')
        filename.write('\\hline \n')

    def write_table_test_cases(self, filename, columns, range_start):
        filename.write('\\textbf{TestCase} & ')

        test_cases_for_requirement = list()
        cnt = 0
        for req in self.requirements[range_start:(range_start + columns)]:
            cnt += 1
            filename.write('\\textbf{')
            filename.write(str(len(self.get_tests_for_requirement(req))))
            test_cases_for_requirement.append(self.get_tests_for_requirement(req))
            filename.write('}')
            if cnt < len(self.requirements[range_start:(range_start + columns)]):
                filename.write(' & ')
        filename.write("\\\\ \n")
        filename.write('\\hline \n')

        test_cases_set = set()
        for test_cases in test_cases_for_requirement:
            for test_case in test_cases:
                test_cases_set.add(test_case)

        for test_case in test_cases_set:
            filename.write('\\textbf{')
            filename.write(test_case)
            filename.write('} & ')
            cnt = 0
            for req in self.requirements[range_start:(range_start + columns)]:
                cnt += 1
                filename.write('\\textbf{')
                #TODO check if test cases is passed failed when applicable
                filename.write('}')
                if cnt < len(self.requirements[range_start:(range_start + columns)]):
                    filename.write(' & ')
            filename.write("\\\\ \n")
            filename.write('\\hline \n')


    def write_table_footer(self, filename):
        filename.write('\\end{longtable} \n')


    def write(self):
        # filename = os.path.dirname(os.path.abspath(__file__)) + "matrix.tex"
        filename = "matrix.tex"
        f = open(filename, 'w')

        columns = 8
        iterations = 0
        while iterations < ceil(float(len(self.requirements)) / float(columns)):
            self.write_table_header(f, columns)
            self.write_table_header_requirements(f, columns, iterations * columns)
            self.write_table_test_cases(f, columns, iterations * columns)
            self.write_table_footer(f)
            iterations += 1

        f.close()