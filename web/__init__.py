from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    from .main import inf_restful as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
