import pprint
import json
import os


def load_elmg_modules(path=u'modules.json'):
    json_data = open(path)
    module_data = json.load(json_data)
    module_names = []
    expanded_module_data = []
    register_paths = []
    
    for module in module_data:
        for instance in range(module[u'instances']):
            new_module_name = '{}_{}'.format(module[u'name'], instance)
            module_names.append(new_module_name)
            
            # make a copy of the module module
            new_module = {}
            new_module[u'name'] = new_module_name
            new_module[u'instance'] = instance
            if module['commit_register'] == "":
                new_module[u'commit_register'] = ""
            else:
                new_module[u'commit_register'] = '{}/{}/{}'.format(module[u'name'], instance, module[u'commit_register'])
          

            new_module [u'registers'] = []
            for register in module [u'registers']:
                reg={}
                reg[u'name'] = register[u'English Name']
                reg[u'module'] = str(new_module_name)
                reg[u'path'] = '{}/{}/{}'.format(module[u'name'], instance, register[u'Sysfs file name'])
                reg[u'min'] = float(register[u'Min'])
                reg[u'max'] = float(register[u'Max'])
                reg[u'read_only'] = register[u'R/W'] != 'R/W'
                reg[u'units'] = register[u'Units']
                reg[u'notes'] = register[u'Description']
                reg['value'] = register[u'Default']
                reg['step'] = register[u'Step']
                 

                register_paths.append(reg[u'path'])
                new_module [u'registers'].append(reg)
            expanded_module_data.append(dict(new_module))  
            
    return expanded_module_data, module_names, register_paths
    
    
    
    
    
if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    modules, module_names, register_paths = load_elmg_modules('axi_modules.json')
    pp.pprint(modules)
    pp.pprint(module_names)
    pp.pprint(register_paths)
    
    for (path) in register_paths:
   
        path = os.path.join('/tmp', path)
        print ("Path %s" % path)
        directory = os.path.dirname(path)
        try: 
            os.makedirs(directory)
        except OSError:
            if not os.path.isdir(directory):
                raise
        with open(path, 'w+') as f:
            f.write(str('0.0'))
    
    
    
