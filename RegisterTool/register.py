import string
from operator import isCallable
class Register(object):
    data_type_map = {u'Integer':u'int', u'Binary':u'bool', u'Bit':u'bool',
                 u'Fixed point string':u'float',u'Float':u'float'
                 }
    proc_dir = "/tmp"
    def __init__(self, sysfs_module_name, register):
        self.name = register[u'English Name']
        self.path = '{}/{}'.format(sysfs_module_name, string.lower(register[u'Sysfs file name']))
        if register[u'Cache write sysfs register'] :
            self.cache_write_register = '{}/{}'.format(sysfs_module_name, string.lower(register[u'Cache write sysfs register']))
        else:
            self.cache_write_register = '' 
        self.cache_register = False
        self.min = float(register[u'Min'])
        self.max = float(register[u'Max'])
        self.read_only = register[u'R/W'] != u'R/W'
        self.units = register[u'Units']
        self.notes = register[u'Description']
        self.value = register[u'Default']
        self.step = register[u'Step']
        if (register[u'Sysfs Format']):
            self.data_type = Register.data_type_map[register[u'Sysfs Format']]
        else:
            self.data_type = u'float'
    
    @staticmethod        
    def setProcDir(dir):        
        Register.proc_dir = dir;
        
            
    def getPath(self):
        return self.path
    
    def getCacheWriteRegister(self):
        return self.cache_write_register
    
    def setCacheRegister(self, value):
        self.cache_register = value
        return 
    
    def isCacheRegister(self):
        return self.cache_register
    
    def hasCacheRegister(self):
        return not self.getCacheWriteRegister() == ""
    
    def isReadOnly(self):
        return self.read_only
    
    def validateLimits(self, value):
        if float(value) >= float(self.min) and float(value) <= float(self.max):
            return True
        print("Value out of range %s:%s (%s - %s)"%(self.path, value, self.min, self.max) )
        return False
    
    def getValue(self):
        return self.value
    
    def update(self):
        if self.isCacheRegister():
            # we can't read the cache registers, they are write only.
            print('cache register: %s ' % self.path)
            return 0
        file_path = Register.proc_dir + '/' + self.path
        value = '0.0'
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    if line.strip():
                        value = line.strip()
                        print('read register: %s = %s' % (file_path, value))
                        break
        except (IOError, OSError):
            print('error reading register: %s ' % file_path)
            return '0'
        self.value = value;
        return self.getValue()
    
    def write(self, value=0):
        if self.isReadOnly():
            return
        if self.isCacheRegister():
            return
        if not self.validateLimits(value):
            return
        file_path =  Register.proc_dir + '/' + self.path
        try:
            print("write %s %s" % (file_path, value))
            with open(file_path, 'w') as f:
                f.write(str(value))
        except (IOError, OSError) as e:
            print("ERROR: Failed to write to %s %s" % (file_path, e))
            pass
            
    def commit(self):
        if self.isCacheRegister():
            file_path = Register.proc_dir + '/' + self.path
            print("commitRegisters %s" % (file_path))
            with open(file_path, 'w') as f:
                f.write(str(1))
