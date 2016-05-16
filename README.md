# spider_news
crawl the current news from sina,baidu and tecent
# ------------------------------------------------------------
# 安装redis并启动
### on mac
    brew install redis
    brew services start redis

# 安装requirement.txt模块包
    pip install -r requirement.txt

# 初始化celery分布式任务队列

# 启动方式：
    celery -A spider_news worker -l info
    celery -A spider_news beat -l info
# ------------------------------------------------------------