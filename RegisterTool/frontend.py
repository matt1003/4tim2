# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, request
from flask_nav.elements import Navbar, View, Subgroup, Link
import pprint

from elmg_modules import load_elmg_modules

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
    modules, module_names , register_paths = load_elmg_modules(app.config['MODULES_PATH'],app.config['ADDRESSES_PATH'])
    module_links()

def getProcDir():
    if 'PROC_DIR' in app.config:
        return app.config['PROC_DIR']
    return "/tmp"


def readRegister(name):
    file_path = getProcDir() + '/' + name
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if not line.strip():
                    print('register: %s = %s' % file_path, line)
    except (IOError, OSError):
        return 0
    return line


def writeRegister(name, value=0):
    
    if name in register_paths:
        file_path = getProcDir() + '/' + name
        try:
            print("write %s %s" % (file_path, value))
            with open(file_path, 'w+') as f:
                f.write(str(value))
        except (IOError, OSError) as e:
            print("ERROR: Failed to write to %s %s" % (file_path, e))
            pass

def commitRegisters(name):
    file_path = getProcDir() + '/' + name
    print("commitRegisters %s" % (file_path))
    with open(file_path, 'w+') as f:
        f.write(str(0))
        f.write(str(1))
        f.write(str(0))


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
    value = -1
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



@frontend.route('/module_commit/<string:mod>', methods=(["POST"]))
def module_commit(mod):
    module_data = getModule(mod)
    commitRegisters(module_data['commit_register'])
    return module(mod)
