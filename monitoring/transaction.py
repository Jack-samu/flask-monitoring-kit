from sqlalchemy import event
import time

from .metrics import TRANSACTION_DURATION, TRANSACTION_ERRORS



def instrument_sqlalchemy(app, db):

    with app.app_context():
        @event.listens_for(db.engine, 'begin')
        def begin_tx(conn):
            conn.info['tx_start'] = time.time()
            conn.info['tx_type'] = 'read_write'

        @event.listens_for(db.engine, 'before_cursor_execute')
        def before_execute(conn, cursor, state, *args):
            if 'tx_start' in conn.info and 'select' in state.lower():
                conn.info['tx_type'] = 'read_only'

        @event.listens_for(db.engine, 'commit')
        def commit_tx(conn):
            if start := conn.info.pop('tx_start', None):
                tx_type = conn.info.pop('tx_type', 'read_write')
                TRANSACTION_DURATION.labels(
                    tx_type = tx_type
                ).observe(time.time() - start)

        @event.listens_for(db.engine, 'rollback')
        def rollback_tx(conn):
            if start := conn.info.pop('tx_start', None):
                tx_type = conn.info.pop('tx_type', 'read_write')
                TRANSACTION_DURATION.labels(
                    tx_type = tx_type
                ).observe(time.time() - start)
                TRANSACTION_ERRORS.labels(error_type='rollback').inc()

        @event.listens_for(db.engine, 'handle_error')
        def handle_error(exception_context):
            exce = str(exception_context.original_exception).lower()
            if 'deadlock' in exec:
                TRANSACTION_ERRORS.labels(error_type='deadlock').inc()
            elif 'timeout' in exec:
                TRANSACTION_ERRORS.labels(error_type='timeout').inc()