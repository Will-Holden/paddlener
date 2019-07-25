from web import create_app
import settings
import os
app = create_app()
from core.consulclient import Server

if __name__ == '__main__':
    server = Server("server")
    server(settings.HOST,settings.PORT, [], "30s")
    app.run(host=settings.HOST, port=settings.PORT)
