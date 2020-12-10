formatter = f"%(asctime)s %(levelname)s [%(module)s:%(lineno)d] %(message)s"

LOG_CONFIG = {"version": 1,
              "disable_existing_loggers": False,
              "formatters": {
                  "default": {
                      "format": formatter}},
              "handlers": {
                  "console": {
                      "class": "logging.StreamHandler",
                      "level": "DEBUG",
                      "formatter": "default",
                      "stream": "ext://sys.stdout"}
              },
              "root": {
                  "level": "DEBUG",
                  "handlers": ["console"]}
              }
