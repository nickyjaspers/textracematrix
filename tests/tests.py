import unittest
from math import ceil

from code_parser import CodeParser
from file_browser import FileBrowser


class TestFileBrowser(unittest.TestCase):
    def test_get_files(self):
        files = FileBrowser.get_files(extension='*.java')
        self.assertEqual(3, len(files))


class TestCodeParser(unittest.TestCase):
    def test_get_requirements_and_test_cases(self):
        files = FileBrowser().get_files(extension='file1.java')
        self.assertTrue(1, len(files))
        parser = CodeParser()
        parser.get_requirements_and_test_cases(files[0])
        self.assertEqual(3, len(parser.req_test_mapping))

    def test_get_requirements_from_requirements_line(self):
        req = CodeParser().get_requirements_from_requirements_line('foo')
        self.assertEqual(0, len(req))

        req = CodeParser().get_requirements_from_requirements_line('// REQ:')
        self.assertEqual(1, len(req))

        req = CodeParser().get_requirements_from_requirements_line('   // REQ:   ')
        self.assertEqual(1, len(req))

        req = CodeParser().get_requirements_from_requirements_line('   // REQ: 1,2,3  ')
        self.assertEqual(3, len(req))
        self.assertEqual('1', req[0])
        self.assertEqual('2', req[1])
        self.assertEqual('3', req[2])

        req = CodeParser().get_requirements_from_requirements_line('// REQ: 1 ,2, 3456  ')
        self.assertEqual(3, len(req))
        self.assertEqual('1', req[0])
        self.assertEqual('2', req[1])
        self.assertEqual('3456', req[2])

    def test_is_test(self):
        self.assertTrue(CodeParser().is_test('@Test'))
        self.assertTrue(CodeParser().is_test(' @Test '))
        self.assertTrue(CodeParser().is_test(' @Test //some comment '))

    def test_get_test_method_name(self):
        self.assertFalse(CodeParser().get_method_name(' no method'))
        self.assertEqual('testTwo', CodeParser().get_method_name('    public void testTwo(){'))
        self.assertEqual('testOne', CodeParser().get_method_name('public void testOne(param){  //comment'))


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
        filename.write('\\begin{longtable}{')
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


class TestMatrixWriter(unittest.TestCase):
    def test_get_requirements_set(self):
        mapping = dict()
        mapping['a'] = ['req1', 'req2', 'req3']
        mapping['b'] = ['req2', 'req3', 'req4']
        writer = MatrixWriter(req_tests_mapping=mapping)
        self.assertEqual(4, len(writer.requirements))
        self.assertEqual(['req1', 'req2', 'req3', 'req4'], writer.requirements)

    def test_get_tests_for_requirement(self):
        mapping = dict()
        mapping['a'] = ['req1', 'req2', 'req3']
        mapping['b'] = ['req2', 'req3']
        mapping['c'] = ['req3', 'req4']
        writer = MatrixWriter(req_tests_mapping=mapping)
        self.assertEqual(['a'], writer.get_tests_for_requirement('req1'))
        self.assertEqual(['a', 'b'], writer.get_tests_for_requirement('req2'))
        self.assertEqual(['a', 'b', 'c'], writer.get_tests_for_requirement('req3'))
        self.assertEqual(['c'], writer.get_tests_for_requirement('req4'))

    def test_write_matrix_file(self):
        mapping = dict()
        mapping['a'] = ['req1', 'req2', 'req3', 'req4', 'req5', 'req6', 'req7', 'req8', 'req9']
        mapping['b'] = ['req7', 'req8', 'req9', 'req10', 'req11', 'req12', 'req13', 'req14', 'req15']
        mapping['c'] = ['req7']
        mapping['d'] = ['req8']
        mapping['e'] = ['req9']
        mapping['f'] = ['req9']
        mapping['g'] = ['req9']
        mapping['h'] = ['req10']
        mapping['i'] = ['req11']
        mapping['j'] = ['req12']
        mapping['k'] = ['req13', 'req14', 'req15', 'req17','req18', 'req19', 'req20', 'req21']
        writer = MatrixWriter(req_tests_mapping=mapping)
        writer.write()

    @unittest.skip("not implemented yet")
    def test_get_result_for_test(self):
        self.assertFalse(True)


if __name__ == '__main__':
    unittest.main()