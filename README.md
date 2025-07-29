<font face="楷体">

## 简介

作为一个附加仓库，旨在实现flask项目的简单监控，关注延迟、流量、错误率和饱和度四个指标，另外针对Mysql方面也有着简单监控。

### 引入项目
```shell
git clone https://github.com/Jack-samu/flask-monitoring-kit.git vendor/flask-monitoring-kit

pip install -e ./vendor/flask-monitoring-kit
```

### 在项目中进行应用：
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

### 部署到docker
项目设定是将mysql部署到docker中的mysql_service，和主体项目相扣。
```shell
# 需要在主体项目中flask-backend以及mysql_service之后启动
sudo docker compose up -d
```