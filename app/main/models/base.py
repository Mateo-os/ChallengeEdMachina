
class BaseModel():

    def to_dict(cls):
        return {c.name: getattr(cls, c.name) for c in cls.__table__.columns}