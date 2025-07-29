from prometheus_client import Counter, Gauge, Histogram


# 请求延迟
REQUEST_DURATION = Histogram(
    'flask_http_request_duration_seconds',
    'HTTP request duration by endpoint',
    ['method', 'endpoint', 'status'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1, 5)
)

# 请求次数
REQUEST_COUNT = Counter(
    'flask_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# 饱和度
SYSTEM_SATURATION = Gauge(
    'flask_system_saturation',
    'System resource saturation'
)

# 错误度
ERROR_COUNT = Counter(
    'flask_http_errors_total',
    'HTTP errors by type',
    ['error_type']
)

# mysql方面指标
TRANSACTION_DURATION = Histogram(
    'mysql_transaction_duration_seconds',
    'Mysql transaction duration',
    ['tx_type'],
    buckets=(0.01, 0.1, 0.5, 1, 5, 10)
)

TRANSACTION_ERRORS = Counter(
    'mysql_transaction_errors_total',
    'Mysql transaction errors',
    ['error_type']
)