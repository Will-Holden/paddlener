from web import create_app
import settings
import os
app = create_app()

if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)
