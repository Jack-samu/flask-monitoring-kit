import time
from flask import request, g
from .metrics import REQUEST_COUNT, REQUEST_DURATION, ERROR_COUNT



def register_prometheus_hooks(app):
    @app.before_request
    def before_request():
        g.monitor_start_time = time.time()
        g.monitor_endpoint = f"{request.method} {request.path}"

    @app.after_request
    def after_request(resp):
        if hasattr(g, 'monitor_start_time') and hasattr(g, 'monitor_endpoint'):
            start_time = g.monitor_start_time
            endpoint = g.monitor_endpoint
            status_code = resp.status_code
            latency = time.time() - start_time
            REQUEST_DURATION.labels(method = request.method,
                                    endpoint = endpoint,
                                    status = status_code).observe(latency)
        
            REQUEST_COUNT.labels(
                method = request.method,
                endpoint = endpoint,
                status = status_code
            ).inc()

            if status_code >= 400:
                ERROR_COUNT.labels(
                    error_type=f'http_{status_code}'
                ).inc()
        
        return resp
    
    @app.errorhandler(Exception)
    def handle_error(e):
        ERROR_COUNT.labels(error_type = 'unhandled_exception').inc()
        raise e