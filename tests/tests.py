import unittest
import fnmatch
import os

'''
IDEA: let xUnit test cases run and scan xml output, 
then for each test case look for associated requirements

IDEA: for every language, a different type of test method searching can be implemented

IDEA: the layout of the requirements can differ


IDEA: for java with junit4 look for java files 
1 -> find a // REQ: 1,2,3 -> DONE
2 -> find first @Test annotation -> DONE
3 -> find test method -> DONE

'''

def get_requirements_from_requirements_line(line, pattern='// REQ:'):
    requirements = []
    if pattern not in line:
        return requirements

    s = line.strip().lstrip(pattern)
    
    reqs = s.split(",")
    for req in reqs:
        requirements.append(req.strip())
    return requirements

def is_test(line, pattern='@Test'):
    if pattern in line.strip():
        return True
    return False

def get_method_name(line, pattern='public void '):
    if pattern not in line:
        return False

    s = line.strip().lstrip(pattern).split('(')
    return s[0]


def get_files(dir=os.path.dirname(os.path.abspath(__file__)), extension='*.*'):
    matches = []
    for root, dirnames, filenames in os.walk(dir):
       for filename in fnmatch.filter(filenames, extension):
           matches.append(os.path.join(root, filename))
    return matches;

def get_requirements_and_testcases(file):
    mapping = dict()
    
    criteriaRequirement = False
    criteriaTest = False
    criteriaMethodName = False
    with open(file) as f:
        lines = f.readlines()
        linecnt = 0
        for line in lines:
            # find requirements
            if criteriaRequirement == False:
                requirements = get_requirements_from_requirements_line(line)
                if len(requirements) > 0:
                    criteriaRequirement = True

            #find test
            if criteriaRequirement == True and criteriaTest == False:
                if is_test(line):
                    criteriaTest = True

            #find method name
            if criteriaRequirement == True and criteriaTest == True and criteriaMethodName == False:
                methodName = get_method_name(line)
                if methodName != False:
                    criteriaMethodName = True                

            # check if al criteria met, add entry in mapping, and reset al criteria
            if criteriaRequirement == True and criteriaTest == True and criteriaMethodName == True:
                mapping[methodName] = requirements
                criteriaRequirement = False
                criteriaTest = False
                criteriaMethodName = False

    return mapping

class TestGetFilesToParse(unittest.TestCase):
    def test_get_files(self):       
        files = get_files(extension='*.java')
        self.assertEqual(3, len(files))

    def test_get_requirements_and_testcases(self):
        files = get_files(extension='file1.java')
        self.assertTrue(1, len(files))
        traceMatrix = get_requirements_and_testcases(files[0])        
        self.assertEqual(3, len(traceMatrix))

    def test_get_requirements_from_requirements_line(self):
        req = get_requirements_from_requirements_line('foo')
        self.assertEqual(0, len(req))

        req = get_requirements_from_requirements_line('// REQ:')
        self.assertEqual(1, len(req))
        
        req = get_requirements_from_requirements_line('   // REQ:   ')
        self.assertEqual(1, len(req))

        req = get_requirements_from_requirements_line('   // REQ: 1,2,3  ')
        self.assertEqual(3, len(req))
        self.assertEqual('1', req[0])
        self.assertEqual('2', req[1])
        self.assertEqual('3', req[2])    

        req = get_requirements_from_requirements_line('// REQ: 1 ,2, 3456  ')
        self.assertEqual(3, len(req))        
        self.assertEqual('1', req[0])
        self.assertEqual('2', req[1])
        self.assertEqual('3456', req[2])
        
    def test_is_test(self):
        self.assertTrue(is_test('@Test'))
        self.assertTrue(is_test(' @Test '))

    def test_get_test_method_name(self):
        self.assertFalse(get_method_name(' no method'))
        self.assertEqual('testTwo', get_method_name('    public void testTwo(){'))
        self.assertEqual('testOne', get_method_name('public void testOne(param){  //comment'))

if __name__ == '__main__':
    unittest.main()