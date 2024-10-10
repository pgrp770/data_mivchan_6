from flask import Flask

from controllers.injury_controller import injury_blueprint

app = Flask(__name__)
app.register_blueprint(injury_blueprint, url_prefix='/api/injury')

if __name__ == '__main__':
    app.run(debug=True)
