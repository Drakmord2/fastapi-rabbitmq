import multiprocessing
import gunicorn.app.base
import uvicorn
from uvicorn.workers import UvicornWorker
from os import getenv
from producer.main import app


def number_of_workers():
    return multiprocessing.cpu_count()


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class Worker(UvicornWorker):
    CONFIG_KWARGS = {"server_header": False, "log_level": "info"}


if __name__ == "__main__":
    reload = False
    if getenv("ENVIRONMENT") != "production":
        reload = True

    if getenv("CLUSTER") in ["KUBERNETES", "LOCAL"]:
        uvicorn.run(
            "producer.main:app",
            host="0.0.0.0",
            port=5000,
            log_level="info",
            reload=reload,
            reload_dirs=["producer"],
            server_header=False,
        )
    else:
        options = {
            "bind": "%s:%s" % ("0.0.0.0", "5000"),
            "workers": number_of_workers(),
            "worker_class": "__main__.Worker",
            "timeout": 120,
        }
        StandaloneApplication(app, options).run()
