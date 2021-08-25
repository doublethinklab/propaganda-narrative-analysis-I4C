import os

from gevent.pywsgi import WSGIServer

from pna import init_app
from pna.dbi import Dbi
from pna.logic import PhillipinesEmbassyLogic


if __name__ == '__main__':
    dbi = Dbi()
    logic = PhillipinesEmbassyLogic(dbi)
    app = init_app(logic)

    if os.environ['DEVELOPMENT'] == '1':
        print('Running development server on localhost.')
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print('Running production WSGI server.')
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
