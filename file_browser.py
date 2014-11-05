import fnmatch
import os


class FileBrowser:
    def __init__(self):
        pass

    @staticmethod
    def get_files(basedir=os.path.dirname(os.path.abspath(__file__)), extension='*.*'):
        matches = []
        for root, dir_names, file_names in os.walk(basedir):
            for filename in fnmatch.filter(file_names, extension):
                matches.append(os.path.join(root, filename))
        return matches