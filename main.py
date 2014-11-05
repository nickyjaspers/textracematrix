import getopt
import sys
import os

from code_parser import CodeParser
from file_browser import FileBrowser


def usage():
    print "==============================================="
    print "Get requirements trace matrix mapping for files"
    print ""
    print "-d [BASEDIR] (default = '.')"
    print "-e [FILE EXTENSION] (default = '*.java')"
    print ""
    print "A mapping is recognized when following pattern is found in a file:"
    print "// REQ: req1, req2"
    print "@Test"
    print "public void TestMethod()"
    print ""
    print "==============================================="


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:e:", ["help", "basedir", "extension"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    extension = '*.java'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--basedir"):
            base_dir = a
        elif o in ("-e", "--extension"):
            extension = a
        else:
            assert False, "unhandled option"

    files = FileBrowser.get_files(basedir=base_dir, extension=extension)
    parser = CodeParser()
    for f in files:
        parser.get_requirements_and_test_cases(f)

    print parser.req_test_mapping


if __name__ == "__main__":
    main()