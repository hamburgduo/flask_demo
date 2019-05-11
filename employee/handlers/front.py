#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models import AllTimeJob, MyUser, MyCompany, PartTimeJob
from ..forms import LoginForm
from .job import job_search
from .company import company_search
import sqlite3

front = Blueprint("front", __name__)


@front.route("/")
def index():
    company_all = MyCompany.query.filter(MyCompany.is_enable.is_(True)).order_by(
        MyCompany.updated_at.desc()
    )
    companies = []
    for c in company_all:
        if c and c.enabled_jobs().count() != 0:
            companies.append(c)
            if len(companies) == 8:
                break
    all_time_jobs = (
        AllTimeJob.query.group_by(AllTimeJob.company_id)
        .order_by(AllTimeJob.updated_at.desc())
        .limit(12)
    )
    part_time_jobs = (
        PartTimeJob.query.group_by(PartTimeJob.company_id)
        .order_by(PartTimeJob.updated_at.desc())
        .limit(12)
    )

    return render_template(
        "index.html",
        active="index",
        all_time_jobs=all_time_jobs,
        part_time_jobs=part_time_jobs,
        companies=companies,
    )


@front.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("front.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user_data = MyUser.query.filter_by(email=form.email.data).first()
        if not user_data:
            user_data = MyCompany.query.filter_by(email=form.email.data).first()
            if not user_data:
                flash("登录信息有误，请重新登录", "danger")
                return redirect(url_for("front.login"))
        if not user_data.check_password(form.password.data):
            flash("登录信息有误，请重新登录", "danger")
            return redirect(url_for("front.login"))
        if not user_data.is_enable:
            flash("该用户不可用，请联系网站管理员", "danger")
            return redirect(url_for("front.login"))
        login_user(user_data, form.remember_me.data)
        flash("登录成功", "success")
        next_page = request.args.get("next")
        return redirect(next_page or url_for("front.index"))
    return render_template("login.html", form=form, active="login")


@front.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("您已经退出登录", "success")
    return redirect(url_for("front.index"))


@front.route("/search")
def search():
    types = request.args.get("type")
    kw = request.args.get("kw")
    cx = sqlite3.connect("employ.db")
    cx.text_factory = str
    # if kw == '' or kw is None:
    #     return render_template('job/index.html')
    if types == "job":
        return job_search()
    else:
        return company_search()
