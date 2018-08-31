import logging

from interproscan_web.application import app

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
