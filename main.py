from web import create_app
import settings
import os
app = create_app()
from core.consulclient import Server

if __name__ == '__main__':
    server = Server("paddleserver")
    server(settings.SERVER_HOST,settings.SERVER_PORT, [], "30s")
    app.run(host=settings.HOST, port=settings.PORT)
