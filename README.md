<font face="楷体">

## 简介

作为一个附加仓库，旨在实现flask项目的简单监控，关注延迟、流量、错误率和饱和度四个指标，另外针对Mysql方面也有着简单监控，更多的还待后续拓展，现在再添加一个k6压测，一并置于docker里面。

**简单架构**
```mermaid
flowchart TB
    %% Application Tier
    subgraph "Application Tier"
        A1["Flask App\n+ /metrics endpoint"]:::app
        subgraph "Flask-Monitoring-Kit\n(Instrumentation Library)"
            M1["metrics.py"]:::code
            M2["middleware.py"]:::code
            M3["saturation.py"]:::code
            M4["transaction.py"]:::code
        end
    end

    %% Monitoring Tier
    subgraph "Monitoring Tier"
        Compose[/Docker Compose\nOrchestration/]:::compose

        subgraph "Prometheus"
            Psrv["Prometheus Server"]:::monitor
            Pcfg["prometheus.yml"]:::config
            Palert["alerts.yml"]:::config
        end

        subgraph "Grafana"
            Gsrv["Grafana Server"]:::monitor
            Gconf["grafana.ini"]:::config
            Gds["prometheus.yml"]:::config
            Gdb["flask_dashboard.json"]:::config
        end

        subgraph "MySQL Exporter"
            Mex["mysqld-exporter"]:::monitor
            Mcfg["my.cnf"]:::config
        end
    end

    %% Data Tier
    subgraph "Data Tier"
        DB["MySQL Database"]:::external
    end

    %% Orchestration relationships
    Compose --> A1
    Compose --> Psrv
    Compose --> Gsrv
    Compose --> Mex

    %% Monitoring flows
    A1 -->|"HTTP /metrics"| Psrv
    Mex -->|"HTTP /metrics"| Psrv
    Mex -->|"TCP"| DB
    Gsrv -->|"HTTP API"| Psrv

    %% Configuration provisioning
    Pcfg -->|"scrape config"| Psrv
    Palert -->|"alert rules"| Psrv
    Gconf -->|"server config"| Gsrv
    Gds -->|"datasource provision"| Gsrv
    Gdb -->|"dashboard provision"| Gsrv
    Mcfg -->|"exporter config"| Mex

    %% Click Events
    click Compose "https://github.com/jack-samu/flask-monitoring-kit/blob/main/docker-compose-monitoring.yml"
    click M1 "https://github.com/jack-samu/flask-monitoring-kit/blob/main/monitoring/metrics.py"
    click M2 "https://github.com/jack-samu/flask-monitoring-kit/blob/main/monitoring/middleware.py"
    click M3 "https://github.com/jack-samu/flask-monitoring-kit/blob/main/monitoring/saturation.py"
    click M4 "https://github.com/jack-samu/flask-monitoring-kit/blob/main/monitoring/transaction.py"
    click Pcfg "https://github.com/jack-samu/flask-monitoring-kit/blob/main/prometheus/prometheus.yml"
    click Palert "https://github.com/jack-samu/flask-monitoring-kit/blob/main/prometheus/alerts.yml"
    click Gconf "https://github.com/jack-samu/flask-monitoring-kit/blob/main/grafana/config/grafana.ini"
    click Gds "https://github.com/jack-samu/flask-monitoring-kit/blob/main/grafana/provisioning/datasources/prometheus.yml"
    click Gdb "https://github.com/jack-samu/flask-monitoring-kit/blob/main/grafana/provisioning/dashboards/flask_dashboard.json"
    click Mcfg "https://github.com/jack-samu/flask-monitoring-kit/blob/main/mysql/my.cnf"

    %% Styles
    classDef app fill:#D6E9FE,stroke:#2B6CB0;
    classDef code fill:#EBF8FF,stroke:#3182CE;
    classDef compose fill:#C6F6D5,stroke:#2F855A;
    classDef monitor fill:#F0FFF4,stroke:#38A169;
    classDef config fill:#FFF5F5,stroke:#E53E3E;
    classDef external fill:#E2E8F0,stroke:#4A5568;
```

### 引入项目
```shell
git clone https://github.com/Jack-samu/flask-monitoring-kit.git vendor/flask-monitoring-kit
```

**修改项目根路径yml部署文件**
```yml
# 添加如下配置
include:
  - ./vendor/flask-monitoring-kit/docker-compose-monitoring.yml
```

**flask项目根路径下添加如下配置**
```
# grafana账号
GF_SECURITY_ADMIN=阿巴巴
GF_SECURITY_ADMIN_PWD=aBb111@
```

### 在flask主体项目中进行应用：
**添加应用代码：**
```python
# 例，在工厂函数中添加
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent/"vendor"/"flask-monitoring-kit"))

def create_app(name='blog-app', config = Config):

    ...
    
    # 监控初始化
    from monitoring import init_metrics
    init_metrics(app, db)

    return app
```

### 命令执行
```shell
# 启动，项目根路径下
docker compose up -d --build

# 停止
docker compose down

# 停止并清理对应build得镜像
docker compose down --rmi local

# 查看某个service日志
docker logs container_name
```

### 预想结果

```shell
# 对于prometheus和mysqld-exporter
```