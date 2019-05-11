# -*- coding: utf-8 -*-

from employee.app import create_app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from employee.models import db, MyUser, MyCompany, Delivery, AllTimeJob, PartTimeJob
from flask_babelex import Babel


app = create_app("development")
admin = Admin(app, name="后台管理系统", template_mode="bootstrap3")
admin.add_view(ModelView(MyUser, db.session, name="用户"))
admin.add_view(ModelView(AllTimeJob, db.session, name="全职"))
admin.add_view(ModelView(PartTimeJob, db.session, name="兼职"))
admin.add_view(ModelView(MyCompany, db.session, name="公司"))
admin.add_view(ModelView(Delivery, db.session, name="简历投递"))
babel = Babel(app)

app.config["BABEL_DEFAULT_LOCALE"] = "zh_CN"


if __name__ == "__main__":
    app.run()
