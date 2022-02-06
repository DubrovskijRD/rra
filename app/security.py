from flask_security import Security, SQLAlchemyUserDatastore

from app.models.db import db
from app.models.user import User, Role


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()

