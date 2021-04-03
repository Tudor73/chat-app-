from flask import Flask 

def create_app():
    app = Flask(__name__)
    app.secret_key ="secret"
    app.config['SECRET_KEY'] = 'secret!'
    
    with app.app_context():

        from .views import view
        from .database import Database

        
        app.register_blueprint(view, url_prefix = "/")

        return app 