from main import app
from settings import APP_PORT

import uvicorn

uvicorn.run(app, port=APP_PORT)
