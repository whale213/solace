from flask import Flask
from views import example

app = Flask(__name__)

# Blueprint views / routes for app
app.register_blueprint(example)

# App Configurations
app.config["PORT_NUMBER"] = 5000 

# Main Compiling 
if __name__ == "__main__":
    app.run(debug=True, port=app.config["PORT_NUMBER"])