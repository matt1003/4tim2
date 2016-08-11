from RegisterTool import create_app, setApp


if __name__ == "__main__":
    # create an app instance
    app = create_app()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    setApp(app)
    app.run(host='0.0.0.0')