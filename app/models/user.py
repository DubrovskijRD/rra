from flask_security import RoleMixin, UserMixin
from sqlalchemy import Column, Table, Integer, Boolean, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship, backref


from .db import db


roles_users = Table(
    'roles_users',
    db.Model.metadata,
    Column('user_id', Integer(), ForeignKey('user.id')),
    Column('role_id', Integer(), ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __str__(self):
        return str(self.name)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean())
    roles = relationship('Role', secondary=roles_users,
                         backref=backref('users', lazy='dynamic'))

    column_labels = dict(
        first_name="Имя",
        last_name="Фамилия",
        model="Модель",
        email="Почта",
        monitoring="Мониторинг",
        password="Пароль",
        active="Активный",
        confirmed_at="CAN",
        roles="Роль",
    )

    def __str__(self):
        return self.email
