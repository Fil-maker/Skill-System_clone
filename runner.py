import os
import app


def run():
    app.app.run(host=os.environ.get("APP_HOST"),
                port=os.environ.get("APP_PORT"),
                debug=int(os.environ.get("APP_DEBUG")))


if __name__ == '__main__':
    run()
