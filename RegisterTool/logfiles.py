import glob
import os


class LogFiles(object):
    def __init__(self):
        return

    def getDataFile(self, dir, file_extension):
        f = glob.glob(dir + "/*." + file_extension)
        datafiles = []
        for p in f:
            datafiles.append(os.path.split(p))
        return sorted(datafiles, key=lambda file: file[1], reverse=True)

    def delete(self, file_path):
        try:
            os.remove(file_path)
        except OSError:
            return False
        return True
