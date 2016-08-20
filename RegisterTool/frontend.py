# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, request
from flask_nav.elements import Navbar, View, Subgroup, Link
import pprint
import os
import json
import time
from register import Register

from elmgModules import loadElmgModules

from forms import RegistersForm
from nav import nav

frontend = Blueprint('frontend', __name__)

pp = pprint.PrettyPrinter(indent=4)

modules = None
module_names = None
register_paths = None


def getRegisterPaths():
    global register_paths
    return register_paths

app = None
def setApp(app_):
    print ("Setting App")
    global app
    app = app_
    Register.setProcDir(getProcDir())


def initModuleRegisters():
    loadRegisters(app.config['MODULES_PATH'], app.config['ADDRESSES_PATH'])
    module_links()

def loadRegisters(modules_path,addresses_path):
    global modules, module_names, register_paths
    modules, module_names , register_paths = loadElmgModules(modules_path,addresses_path)

def getProcDir():
    global app
    if  app and 'PROC_DIR' in app.config:
        return app.config['PROC_DIR']
    return "/tmp"



def module_links():
    links = []
    for mod in module_names:
        links.append(Link(mod, '/module/' + mod))
    nav.register_element('frontend_top',
                         Navbar(
                                View('Home', '.index'),
                                View('File', 'frontend.file'),
                                Subgroup('Modules', *links)
                                )
                         )


def getModule(module_name):
    return next((l for l in modules if l['name'] == module_name), None)

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@frontend.route('/')
def index():
    return render_template('index.html')




@frontend.route('/file/', methods=(['GET']))
def file():
    return render_template('file.html')

@frontend.route('/submit_file/', methods=(['GET', 'POST']))
def submit_file():
    pp.pprint(request.form)
    if request.method == 'POST':
        if  request.form['action'] == 'Save':
            save(app.config['DATA_FILE'])
        if  request.form['action'] == 'Restore':
            load(app.config['DATA_FILE'])

    return render_template('file.html')

@frontend.route('/module/<string:mod>', methods=(['GET']))
def module(mod):
    form = RegistersForm()
    module_data = getModule(mod)

    for reg in module_data['registers']:
        reg.update()

    return render_template('module.html',
                           module={'name':module_data['name']},
                           registers=module_data['registers'], form=form)




@frontend.route('/submit/<string:mod>', methods=(['GET', 'POST']))
def submit(mod):
#     pp.pprint(request.form)
    if request.method == 'POST' and request.form['submit'] == 'Submit':
        # write the data to the registers.
        data = request.form
        for register_path in data:
            if register_path in register_paths:
                register_paths[register_path].write(data[register_path])
        # now write to the cache commit registers.
        for register_path in data:
            if register_path in register_paths:
                register_paths[register_path].commit()
    return module(mod)

def createTempFilesytem():
    for path, reg in register_paths.iteritems():
        file_path = os.path.join('/tmp', path)
        directory = os.path.dirname(file_path)
        try:
            os.makedirs(directory)
        except OSError:
            if not os.path.isdir(directory):
                raise
        if not os.path.isfile(file_path):
            with open(file_path, 'w+') as f:
                print ('Creating temp register path %s with default value of %s' % (file_path, reg['value']))
                f.write(str(reg['value']))


def save(file_path = "/tmp/data.elmg"):
    values = {}
    values[u'version']="1.0.0"
    values[u'raw_time']=  time.time()
    values[u'date']=time.asctime( time.localtime(time.time()) )
    for path, reg in getRegisterPaths().iteritems():
        values[path] = reg.update()
    with open(file_path, 'w') as outfile:
        json.dump(values, outfile,  sort_keys=True,indent=4, separators=(',', ': '))

def load(file_path = "/tmp/data.elmg"):
    json_data = open(file_path)
    values = json.load(json_data)
    for path, value in values.iteritems():
        if path in register_paths:
            register_paths[path].write(value)

    #Write all the cache registers.
    for path, value in values.iteritems():
        if path in register_paths:
            register_paths[path].commit()

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    loadRegisters("modules.json","addresses.csv")
    createTempFilesytem()
    save('/tmp/data.elmg')
    load('/tmp/data.elmg')
