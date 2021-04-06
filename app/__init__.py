from flask import Flask 


def create_app():
    # function used to initialize the flask app with the following settings
    app = Flask(__name__)
    app.secret_key ="secret"
    app.config['SECRET_KEY'] = 'secret!'
    
    with app.app_context():

        from .views import view  
        from .database import Database 

        
        app.register_blueprint(view, url_prefix = "/")

        return app 