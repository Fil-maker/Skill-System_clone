import os
import api


def run():
    api.app.run(host=os.environ.get("API_HOST"),
                port=os.environ.get("API_PORT"),
                debug=int(os.environ.get("API_DEBUG")))


if __name__ == '__main__':
    run()
