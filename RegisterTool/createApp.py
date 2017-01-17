# Welcome to the Flask-Bootstrap sample application. This will give you a
# guided tour around creating an application using Flask-Bootstrap.
#
# To run this application yourself, please install its requirements first:
#
#   $ pip install -r sample_app/requirements.txt
#
# Then, you can actually run the application.
#
#   $ flask --app=sample_app dev
#
# Afterwards, point your browser to http://localhost:5000, then check out the
# source.


from flask import Flask

from flask_bootstrap import Bootstrap

from frontend import frontend, setApp, initModuleRegisters
from nav import nav


def createApp(configfile=None):
    # We are using the "Application Factory"-pattern here, which is described
    # in detail inside the Flask docs:
    # http://flask.pocoo.org/docs/patternslo/appfactories/

    app = Flask(__name__)

    # Install our Bootstrap extensioappappn
    Bootstrap(app)

    # Our application uses blueprints as well; these go well with the
    # application factory. We already imported the blueprint, now we just need
    # to register it:
    app.register_blueprint(frontend)

    app.config.from_object('config')

    # Because we're security-conscious developers, we also hard-code disabling
    # the CDN support (this might become a default in later versions):
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    setApp(app)
    initModuleRegisters()

    # We initialize the navigation as well
    nav.init_app(app)
    return app


if __name__ == "__main__":
    # create an app instance
    app = create_app()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    setApp(app)

    app.run(debug=True)
