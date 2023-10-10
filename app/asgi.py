from fastapi import FastAPI
from database import db
from main.controller import lead_controller,course_controller

PROJECT_NAME = 'ChallengeEdMachina'

def create_app():
    app = FastAPI(
        title='Challenge',
    )

    db.init_app(app)

    app.include_router(lead_controller, prefix='/leads', tags=['leads'])

    app.include_router(course_controller, prefix='/courses', tags=['courses'])

    return app

app = create_app()

