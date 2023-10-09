from fastapi import FastAPI
from app.database import db
from app.main.controller import user_controller, auth_controller

PROJECT_NAME = 'ChallengeEdMachina'

def create_app(config_name):
    app = FastAPI(
        title='Challenge',
    )

    db.init_app(app)

    app.include_router(user_controller.router, prefix='/users', tags=['users'])

    app.include_router(auth_controller.router, prefix='/auth', tags=['auth'])

    return app