from flask import Flask
from prometheus_client import make_wsgi_app

from .middleware import register_prometheus_hooks
from .saturation import SaturationMonitor
from .transaction import instrument_sqlalchemy



def init_metrics(app: Flask, db):
    @app.route('/metrics')
    def metrics():
        return make_wsgi_app()
    
    register_prometheus_hooks(app)
    instrument_sqlalchemy(app, db)
    monitor = SaturationMonitor()