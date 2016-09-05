import pprint
import json
import os
import csv
import string
from pip._vendor.requests.utils import address_in_network
from register import Register




def loadElmgModules(modules_path=u'modules.json', addresses_path=u'addresses.csv'):
    json_data = open(modules_path)
    module_data = json.load(json_data)
    module_names = []
    expanded_module_data = []
    register_paths = {}
    address_map = {}
    type_map = {}
    
    with open(addresses_path, u'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            address_map[str(row[1])] = row[0]
            type_map[str(row[1])] = row[2]
    
    for module in module_data:
        for instance in range(module[u'instances']):
            new_module_name = '{}_{}'.format(module[u'name'], instance)
            module_names.append(new_module_name)
            
            # make a copy of the module module
            new_module = {}
            new_module[u'name'] = new_module_name
            new_module[u'instance'] = instance
            new_module [u'registers'] = []
            for register in module [u'registers']:
                if register[u'Sysfs'] != 'N':
                    mod_name = '{}_{}'.format(module[u'name'], instance)
                    sysfs_module_name = '{}.{}'.format(string.lower(address_map[mod_name]), type_map[mod_name])
                    reg = Register(sysfs_module_name, register)
                    register_paths[reg.getPath()] = reg
                    new_module [u'registers'].append(reg)
            expanded_module_data.append(dict(new_module))  
            for key, reg in register_paths.iteritems():
                if  reg.hasCacheRegister():
                    register_paths[reg.getCacheWriteRegister()].setCacheRegister(True)
                                                                                 
    return expanded_module_data, module_names, register_paths
    
  



    
    
if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    modules, module_names, register_paths = loadElmgModules(u'modules.json', u'addresses.csv')
    pp.pprint(modules)
    pp.pprint(module_names)
    pp.pprint(register_paths)
    
    
    
    
