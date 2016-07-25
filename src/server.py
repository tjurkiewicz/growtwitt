import os
import cherrypy

import growbots.wsgi


if __name__ == '__main__':
    cherrypy.server.unsubscribe()

    cherrypy.tree.graft(growbots.wsgi.application, "/")

    server = cherrypy._cpserver.Server()

    # might be configurable as well
    server.socket_host = '0.0.0.0'
    server.socket_port = int(os.environ.get('PORT', '8080'))
    server.thread_pool = 30

    server.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
