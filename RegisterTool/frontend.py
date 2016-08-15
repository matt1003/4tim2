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

from elmgModules import loadElmgModules

from forms import RegistersForm
from nav import nav

frontend = Blueprint('frontend', __name__)

pp = pprint.PrettyPrinter(indent=4)

modules = None
module_names = None
register_paths = None


app = None
def setApp(app_):
    print ("Setting App")
    global app
    app = app_


def initModuleRegisters():
    global modules, module_names, register_paths
    modules, module_names , register_paths = loadElmgModules(app.config['MODULES_PATH'], app.config['ADDRESSES_PATH'])
    module_links()

def getProcDir():
    if 'PROC_DIR' in app.config:
        return app.config['PROC_DIR']
    return "/tmp"


def readRegister(name):
    if isCacheRegister(name):
        # we can't read the cache registers, they are write only.
        print('cache register: %s ' % name)
        return 0
    file_path = getProcDir() + '/' + name
    value = '0.0'
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                   value = line.strip()
                   print('register: %s = %s' % (file_path, value))
                   break
                print('$$$ register:  %s' %  file_path)
    except (IOError, OSError):
        print('error reading register: %s ' % file_path)
        return '0'
    return value

def writeRegister(name, value=0):
    if isCacheRegister(name):
        # we can't write the cache registers like this we must use, commitRegisters()
        commitRegisters (name)
    if name in register_paths:
        file_path = getProcDir() + '/' + name
        try:
            print("write %s %s" % (file_path, value))
            with open(file_path, 'w') as f:
                f.write(str(value))
        except (IOError, OSError) as e:
            print("ERROR: Failed to write to %s %s" % (file_path, e))
            pass

def commitRegisters(name):
    file_path = getProcDir() + '/' + name
    print("commitRegisters %s" % (file_path))
    with open(file_path, 'w') as f:
        f.write(str(1))


def module_links():
    links = []
    for mod in module_names:
        links.append(Link(mod, '/module/' + mod))
    nav.register_element('frontend_top',
                         Navbar(
                                View('Home', '.index'),
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

@frontend.route('/module/<string:mod>', methods=(['GET']))
def module(mod):
    form = RegistersForm()
    module_data = getModule(mod)

    for reg in module_data['registers']:
        reg['value'] = readRegister(reg['path'])

    return render_template('module.html',
                           module={'name':module_data['name']},
                           registers=module_data['registers'], form=form)

def isCacheRegister(register_path):
    if register_path in register_paths:
        return register_paths[register_path][u'cache_register']
    return False

@frontend.route('/submit/<string:mod>', methods=(['GET', 'POST']))
def submit(mod):
    data = request.form
    if request.method == 'POST':
        # write the data to the registers.
        for register_path in data:
            if not isCacheRegister(register_path):
                writeRegister(register_path, data[register_path])
        # now write to the cache commit registers.
        for register_path in data:
            if isCacheRegister(register_path):
                commitRegisters(register_path)
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
