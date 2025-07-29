import threading
import time
import psutil


from .metrics import SYSTEM_SATURATION


class SaturationMonitor:
    def __init__(self, db=None, interval=30):
        self.db = db
        self.interval = interval
        self._running = False

    def _collect_metrics(self):
        # CPU利用率
        SYSTEM_SATURATION.labels(resource_type='cpu').set(
            psutil.cpu_percent()
        )

        # 内存利用率
        SYSTEM_SATURATION.labels(resource_type='memory').set(
            psutil.virtual_memory().percent()
        )

        # 数据库连接
        if self.db and hasattr(self.db.engine, 'pool'):
            pool = self.db.engine.pool
            SYSTEM_SATURATION.labels(resource_type='db_connections').set(
                pool.checkedout() / pool.size() *100
            )

    def start(self):
        self._running = True
        def run():
            while self._running:
                self._collect_metrics()
                time.sleep(self.interval)
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    def stop(self):
        self._running = False