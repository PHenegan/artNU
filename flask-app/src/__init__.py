# Some set up for the application 

from flask import Flask
from flaskext.mysql import MySQL

# create a MySQL object that we will use in other parts of the API
db = MySQL()

def create_app():
    app = Flask(__name__)
    
    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'

    # these are for the DB object to be able to connect to MySQL. 
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = open('/secrets/db_password.txt').readline().strip()
    app.config['MYSQL_DATABASE_HOST'] = 'db'
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_DB'] = 'ArtNU'  # Change this to your DB name

    # Initialize the database object with the settings above. 
    db.init_app(app)
    
    # Add a default route
    @app.route("/")
    def welcome():
        return "<h1>Welcome to the art.NU by Professor Fontenot's favorite team</h1>"

    # Import the various routes
    from src.views import views
    from src.artists.artists import artists
    from src.commission_types.commission_types import commission_types
    from src.images.images import images
    from src.clients.clients import clients

    # Register the routes that we just imported so they can be properly handled

    app.register_blueprint(artists, url_prefix='/artists')
    app.register_blueprint(commission_types, url_prefix='/commission_types')
    app.register_blueprint(images, url_prefix='/images')
    app.register_blueprint(clients, url_prefix='/clients')


    return app