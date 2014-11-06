import unittest

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
        self.requirements = set()

    def get_requirements_set(self):
        for key in self.req_tests_mapping:
            for req in self.req_tests_mapping[key]:
                self.requirements.add(req)


class TestMatrixWriter(unittest.TestCase):
    def test_write_simple_matrix(self):
        mapping = dict()
        mapping['a'] = ['req1', 'req2', 'req3']
        mapping['b'] = ['req2', 'req3', 'req4']
        writer = MatrixWriter(req_tests_mapping=mapping)
        writer.get_requirements_set()
        self.assertEqual(4, len(writer.requirements))
        self.assertEqual(['req1', 'req2', 'req3', 'req4'], sorted(writer.requirements))


if __name__ == '__main__':
    unittest.main()