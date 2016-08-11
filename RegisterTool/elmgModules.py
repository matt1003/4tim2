import pprint
import json
import os
import csv
from pip._vendor.requests.utils import address_in_network

data_type_map = {u'Integer':u'int',u'Binary':u'bool', u'Fixed point string':u'float'}


def loadElmgModules(modules_path=u'modules.json', addresses_path=u'addresses.csv'):
    json_data = open(modules_path)
    module_data = json.load(json_data)
    module_names = []
    expanded_module_data = []
    register_paths = {}
    address_map = {}
    
    with open(addresses_path, u'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            address_map[str(row[1])] = row[0]
    
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
                reg={}
                mod_name = '{}_{}'.format(module[u'name'],instance)
                sysfs_module_name = '{}.{}'.format(address_map[mod_name],mod_name)
                reg[u'name'] = register[u'English Name']
                reg[u'module'] = str(new_module_name)
                reg[u'path'] = '{}/{}'.format(sysfs_module_name, register[u'Sysfs file name'])
                if register[u'Cache write sysfs register'] :
                    reg[u'cache_write_register'] = '{}/{}'.format(sysfs_module_name, register[u'Cache write sysfs register'])
                else:
                    reg[u'cache_write_register'] = '' 
                reg[u'cache_register'] = False
                reg[u'min'] = float(register[u'Min'])
                reg[u'max'] = float(register[u'Max'])
                reg[u'read_only'] = register[u'R/W'] != u'R/W'
                reg[u'units'] = register[u'Units']
                reg[u'notes'] = register[u'Description']
                reg[u'value'] = register[u'Default']
                reg[u'step'] = register[u'Step']
                reg[u'data_type'] = data_type_map[register[u'Sysfs Format']]

                register_paths[reg[u'path']] = reg
                new_module [u'registers'].append(reg)
            expanded_module_data.append(dict(new_module))  
            for key, reg in register_paths.iteritems():
                if  reg[u'cache_write_register']:
                    register_paths[reg[u'cache_write_register']][u'cache_register'] = True
    return expanded_module_data, module_names, register_paths
    
    

    
    
if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    modules, module_names, register_paths = load_elmg_modules(u'modules.json',u'addresses.csv')
    pp.pprint(modules)
    pp.pprint(module_names)
    pp.pprint(register_paths)
    
    createTempFilesytem()
    
    
    
