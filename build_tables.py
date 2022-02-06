from app.config import ADMIN_EMAIL, ADMIN_PASS
from app.app import create_app

from app.models.db import db
from app.models.user import *
from app.models.rra import *

from app.consts import Roles, CheckStatusList, AutoCategoryList

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        admin_role_id = None
        for role in Roles:
            role_db = Role(name=role.value, description=role.value)
            db.session.add(role_db)
            try:
                db.session.commit()
            except Exception as err:
                db.session.rollback()
                continue
            if role == Roles.ADMIN:
                admin_role_id = role_db.id

        if admin_role_id:
            app.extensions['security'].datastore.create_user(
                email=ADMIN_EMAIL, password=ADMIN_PASS, roles=[Roles.ADMIN.value]
            )
            db.session.commit()

        for status in CheckStatusList:
            status_db = CheckStatus(name=status.value)
            db.session.add(status_db)
            try:
                db.session.commit()
            except Exception as err:
                db.session.rollback()

        for category in AutoCategoryList:
            category_db = AutoCategory(name=category.value)
            db.session.add(category_db)
            try:
                db.session.commit()
            except Exception as err:
                db.session.rollback()






