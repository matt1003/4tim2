from RegisterTool.createApp import createApp 
from RegisterTool.frontend import  setApp, createTempFilesytem


if __name__ == "__main__":
    # create an app instance
    app = createApp()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    setApp(app)
    if app.config['PROC_DIR'] == '/tmp':
        createTempFilesytem()
    app.run(debug=1, host='0.0.0.0')
