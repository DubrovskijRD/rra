from flask import abort, redirect, url_for, request
from flask_security import current_user
from flask_admin import expose
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.filters import FilterInList
from sqlalchemy import inspect

from app.consts import Roles
from app.models.db import db
from app.models.user import Role, User
from app.models.rra import RRA, AutoCategory, CheckStatus


class RelatedFilter(FilterInList):

    def __init__(self, column, name, options=None, data_type=None, rel_model=None):
        self.rel_model = rel_model
        super().__init__(column, name, options, data_type)

    def apply(self, query, value, alias=None):
        return query.join(self.rel_model).filter(self.rel_model.name.in_(value))

    def get_options(self, view):
        try:
            return [(rel.name, rel.name) for rel in self.rel_model.query.order_by(self.rel_model.name)]
        except RuntimeError:
            # for first start
            return []


class MyModelView(sqla.ModelView):
    roles = None
    can_edit = False
    can_create = False
    can_delete = False
    need_filter_refresh = False

    column_auto_select_related = True
    delete_roles = {Roles.ADMIN.value}
    edit_roles = {Roles.ADMIN.value, Roles.EDITOR.value}
    create_roles = {Roles.ADMIN.value, Roles.EDITOR.value}

    def __init__(self, model, session, roles=None, **kwargs):

        if roles:
            self.roles = roles
        else:
            self.roles = self.roles or []
        if hasattr(model, 'column_labels'):
            self.column_labels = model.column_labels

        related = inspect(model).relationships
        self.column_select_related_list = related.keys()
        # # self.column_select_related_list = inspect(model).relationships.keys()
        f_keys = [key.parent.name for key in model.__table__.foreign_keys] + ['id']
        self.column_searchable_list = [c.name for c in model.__table__.columns if c.name not in f_keys]
        self.column_list = [*self.column_searchable_list, *related.keys()]
        filters = self.column_searchable_list
        if hasattr(model, 'relationship_filters'):
            self.need_filter_refresh = True
            filters = [
                *filters,
                *[
                    RelatedFilter(column, self.column_labels.get(column), rel_model=rel_model)
                    for column, rel_model in model.relationship_filters
                ]
            ]
        self.column_filters = filters
        super().__init__(model, session, **kwargs)

    @expose('/')
    def index_view(self):
        if self.need_filter_refresh:
            print("refresh")
            self._refresh_filters_cache()
        return super().index_view()

    def is_accessible(self):
        self.can_edit = False
        self.can_create = False
        self.can_delete = False

        condition = (current_user.is_active and
                     current_user.is_authenticated)
        if self.roles:
            condition = condition and any(current_user.has_role(role) for role in self.roles)
        if not condition:
            return condition
        for role in self.delete_roles:
            if current_user.has_role(role):
                self.can_delete = True
                break
        for role in self.create_roles:
            if current_user.has_role(role):
                self.can_create = True
                break
        for role in self.edit_roles:
            if current_user.has_role(role):
                self.can_edit = True
                break
        print(current_user)
        return condition

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


def admin_views():
    return (
        MyModelView(User, db.session, roles=[Roles.ADMIN.value], name="Пользователи"),
        # MyModelView(Role, db.session, roles=[Roles.ADMIN.value]),

        MyModelView(RRA, db.session, name="РРА"),

        # uncomment for add catalog control
        # MyModelView(AutoCategory, db.session, roles=[Roles.ADMIN.value, Roles.EDITOR.value],
        #             category="Каталоги", name="Категории авто"),
        # MyModelView(CheckStatus, db.session, roles=[Roles.ADMIN.value, Roles.EDITOR.value],
        #             category="Каталоги", name="Да/Нет"),
    )