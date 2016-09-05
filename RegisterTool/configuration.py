
import json
from time import localtime, strftime, asctime
import glob
import os 
import pprint

class Configuration(object):
    register_paths_ = None
    def __init__(self, register_paths):
        Configuration.register_paths_ = register_paths
    def getDataFile(self, dir, file_extension):
        f = glob.glob(dir + "/*." + file_extension)
        datafiles = []
        for p in f:
            datafiles.append(os.path.split(p))
        return sorted (datafiles, key=lambda file: file[1], reverse=True)
            
        
    def save(self, path='/tmp', ext='elmg'):
      
        values = {}
        values[u'version'] = "1.0.0"
        now = localtime()
        values[u'date'] = asctime(now)
        file_path = path + strftime("/data-%Y-%m%d%H%M%S.", now) + ext
        
        for path, reg in Configuration.register_paths_.iteritems():
            values[path] = reg.update()
        try:
            with open(file_path, 'w') as outfile:
                json.dump(values, outfile, sort_keys=True, indent=4, separators=(',', ': '))
                return os.path.split(file_path)[1]
        except IOError:
            return ""

    def load(self, file_path="/tmp/data.elmg"):
        try:
            json_data = open(file_path)
            values = json.load(json_data)
       
            for path, value in values.iteritems():
                if path in Configuration.register_paths_:
                    Configuration.register_paths_[path].write(value)
        
            # Write all the cache registers.
            for path, value in values.iteritems():
                if path in Configuration.register_paths_:
                    Configuration.register_paths_[path].commit()
        except IOError:
            return False
        return True
                
    def delete(self, file_path):
        try:
            os.remove(file_path)
        except OSError:
            return False
        return True
        
