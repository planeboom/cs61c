import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,  # 不覆盖默认配置
    "formatters": {  # 日志输出样式
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",  # 控制台输出
            "level": "INFO",
            "formatter": "default",
        },
        "log_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default",   # 日志输出样式对应formatters
            "filename": "app/storage/logs/flask.log",  # 指定log文件目录
            "maxBytes": 20*1024*1024,   # 文件最大20M
            "backupCount": 10,          # 最多10个文件
            "encoding": "utf8",         # 文件编码
        },

    },
    "root": {
        "level": "DEBUG",  # # handler中的level会覆盖掉这里的level
        "handlers": ["console", "log_file"],
    },
}
)

app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.WARNING)
app.json.ensure_ascii = False
app.config.from_object('config')
db = SQLAlchemy(app)
from app import views,models