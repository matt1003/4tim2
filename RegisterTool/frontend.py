# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template,  request
from flask_nav.elements import Navbar, View, Subgroup, Link
import pprint

from elmg_modules import load_elmg_modules

from forms import RegistersForm
from nav import nav

frontend = Blueprint('frontend', __name__)

pp = pprint.PrettyPrinter(indent=4)

modules = None
module_names = None
paths = None


app = None
def setApp(app_):
    print ("Setting App")
    global app
    app = app_


def init_module_registers(moduls_path):
    global modules,    module_names,    paths
    modules, module_names , paths = load_elmg_modules(moduls_path)
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
    file_path = getProcDir() + '/' + name
    print("write %s %s" % (file_path, value))
    with open(file_path, 'w+') as f:
        f.write(str(value))

def commitRegisters(name):
    file_path = getProcDir() + '/' + name
    print("commitRegisters %s" % (file_path))
    with open(file_path, 'w+') as f:
        f.write(str(0))
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
    with_commit = not module_data['commit_register'] == ""

    return render_template('module.html',

                           module={'name':module_data['name'],
                           'with_commit':with_commit},
                           registers=module_data['registers'], form=form)


@frontend.route('/submit/<string:mod>', methods=(['GET', 'POST']))
def submit(mod):
    data = request.form
    if request.method == 'POST':
        writeRegister(data['register'], data['value'])
    return module(mod)


@frontend.route('/submit_bool/<string:mod>', methods=(['GET', 'POST']))
def submit_bool(mod):
    data = request.form
    if request.method == 'POST':
        if  request.form.getlist('check') :
            writeRegister(data['register'], 1)
        else:
            writeRegister(data['register'], 0)
    return module(mod)



@frontend.route('/module_commit/<string:mod>', methods=(["POST"]))
def module_commit(mod):
    module_data = getModule(mod)
    commitRegisters(module_data['commit_register'])
    return module(mod)
