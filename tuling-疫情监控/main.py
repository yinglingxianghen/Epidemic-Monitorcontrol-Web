from flask import Flask
app = Flask(__name__)
from apps.index.view import a1
app.register_blueprint(a1)


REDIS_CONF = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 1
}
app.config.update({'REDIS_CONF': REDIS_CONF})

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=5000)


