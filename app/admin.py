import flask_admin


admin = flask_admin.Admin(name="РРА", base_template='my_master.html', template_mode='bootstrap4',
                          index_view=flask_admin.AdminIndexView(name="Главная", url='/rra'), url='/rra')
