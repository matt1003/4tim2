# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, request, flash, send_from_directory, redirect, url_for
from flask_nav.elements import Navbar, View, Subgroup, Link
from werkzeug.utils import secure_filename
import pprint
import os

from register import Register
from configuration import Configuration

from elmgModules import loadElmgModules

from forms import RegistersForm
from nav import nav

frontend = Blueprint('frontend', __name__)

pp = pprint.PrettyPrinter(indent=4)

modules = None
module_names = None
register_paths = None
configuration = None


ALLOWED_EXTENSIONS = set(['elmg'])


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

def loadRegisters(modules_path, addresses_path):
    global modules, module_names, register_paths, configuration
    modules, module_names , register_paths = loadElmgModules(modules_path, addresses_path)
    configuration = Configuration(register_paths)

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
                                View('File', 'frontend.fileForm'),
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


@frontend.route('/tmp/<path:filename>')
def download_file(filename):
    pp.pprint(filename)
    return send_from_directory(app.config['DATA_FILE_PATH'],
                               filename, as_attachment=True)


@frontend.route('/fileForm/', methods=(['GET']))
def fileForm():
    f = configuration.getDataFile(app.config['DATA_FILE_PATH'], app.config['DATA_FILE_EXTENSION'])
    return render_template('file.html', files=f)

@frontend.route('/submit_file/', methods=(['GET', 'POST']))
def submit_file():
    pp.pprint(request.form)
    if request.method == 'POST':
        if  request.form['action'] == 'Save':
            f = configuration.save(app.config['DATA_FILE_PATH'], app.config['DATA_FILE_EXTENSION'])
            if f != "":
                flash('Configuration {} Saved'.format(f))
            else:
                flash('Failed to save configuration')
                  
        if  request.form['action'] == 'Restore':
            if 'files' in request.form.keys():
                if configuration.load(app.config['DATA_FILE_PATH'] + "/" + request.form['files']):
                    flash('Configuration {} restored'.format(request.form['files']))
                else:
                    flash('Failed to restore configuration {}'.format(request.form['files']))
            else:
                flash('No file selected ')
                
        if  request.form['action'] == 'Delete':
            if 'files' in request.form.keys():
                if configuration.delete(app.config['DATA_FILE_PATH'] + "/" + request.form['files']):
                    flash('Configuration {} Deleted'.format(request.form['files']))
                else:
                    flash('Failed to delete configuration {}'.format(request.form['files']))
            else:
                flash('No file selected ')
        if  request.form['action'] == 'Upload':
            print('Upload')
            upload_file()
    return fileForm()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload_file():
#     if request.method == 'POST':    
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return  fileForm()
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return fileForm()
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        f = file.save(os.path.join(app.config['DATA_FILE_PATH'], filename))
        if f =='':
            flash(' Upload failed: {}'.format(file.filename))
        else:
            flash(' Upload success: {}'.format(file.filename))
        return redirect(url_for('frontend.fileForm', filename=filename))
    else:
        print('Upload unsupported')
        flash('Missing or unsupported file type: {}'.format(file.filename))
    return fileForm()
            
# @frontend.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['DATA_FILE_PATH'], filename)
    
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
    if request.method == 'POST' and request.form['submit'] == 'Start Motor':
        os.system(app.config['START_SCRIPT'])
    if request.method == 'POST' and request.form['submit'] == 'Stop Motor':
        os.system(app.config['STOP_SCRIPT'])        
    if request.method == 'POST' and request.form['submit'] == 'Start Dlog':
        os.system(app.config['DLOG_SCRIPT'])        
    if request.method == 'POST' and request.form['submit'] == 'DTC On':
        os.system(app.config['DTCON_SCRIPT'])                
    if request.method == 'POST' and request.form['submit'] == 'DTC Off':
        os.system(app.config['DTCOFF_SCRIPT'])                
    if request.method == 'POST' and request.form['submit'] == 'Position Control':
        os.system(app.config['PSNC_SCRIPT'])                
    if request.method == 'POST' and request.form['submit'] == 'Speed Control':
        os.system(app.config['SPDC_SCRIPT'])                        
        

        
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
            try:
                with open(file_path, 'w+') as f:
                    print ('Creating temp register path %s with default value of %s' % (file_path, reg.getValue()))
                    f.write(str(reg.getValue()))
            except IOError:
                pass




if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    loadRegisters("modules.json", "addresses.csv")
    createTempFilesytem()
    save('/tmp/data.elmg')
    load('/tmp/data.elmg')
