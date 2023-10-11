from .lead import Lead, CourseAttempt
from .course import Course

from database import db
metadata = db.Model.metadata