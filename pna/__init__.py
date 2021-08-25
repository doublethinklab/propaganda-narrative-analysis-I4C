from flask import Flask

from pna.config import Config
from pna.logic import Logic


class PropagandaNarrativeAnalysis(Flask):

    def set_logic(self, logic: Logic):
        self.logic = logic


def init_app(logic: Logic):
    app = PropagandaNarrativeAnalysis(
        __name__, static_url_path='/pna/pna/static')
    app.config.from_object(Config)
    app.set_logic(logic)

    with app.app_context():
        from . import routes

        from .plotlydash import init_dashboard
        app = init_dashboard(app)

    return app
