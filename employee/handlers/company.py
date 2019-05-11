#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
    abort,
)
from flask_login import current_user
from sqlalchemy import func
from ..decorators import company_required
from ..forms import RegisterCompanyForm, CompanyDetailForm
from ..models import MyCompany, AllTimeJob, Delivery, db, PartTimeJob


company = Blueprint("company", __name__, url_prefix="/company")


@company.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("front.index"))
    form = RegisterCompanyForm()
    if form.validate_on_submit():
        form.create_company()
        flash("注册成功，请登录", "success")
        return redirect(url_for("front.login"))
    return render_template(
        "company/register.html", form=form, active="company_register"
    )


@company.route("/")
def index():
    page = request.args.get("page", default=1, type=int)
    kw = request.args.get("kw")
    flt = {MyCompany.is_enable is True}
    if kw is not None and kw != "":
        flt.update({MyCompany.name.ilike("%{}%".format(kw))})
    pagination = (
        MyCompany.query.filter(*flt)
        .order_by(MyCompany.updated_at.desc())
        .paginate(
            page=page,
            per_page=current_app.config["COMPANY_INDEX_PER_PAGE"],
            error_out=False,
        )
    )
    return render_template(
        "company/index.html", pagination=pagination, kw=kw, active="company"
    )


@company.route("/<int:company_id>")
def detail(company_id):
    company_obj = MyCompany.query.get_or_404(company_id)
    if not company_obj.is_enable:
        abort(404)
    if request.args.get("job"):
        page = request.args.get("page", default=1, type=int)
        pagination = (
            company_obj.enabled_jobs()
            .order_by(AllTimeJob.updated_at.desc())
            .paginate(
                page=page,
                per_page=current_app.config["COMPANY_DETAIL_PER_PAGE"],
                error_out=False,
            )
        )
        return render_template(
            "company/detail.html",
            pagination=pagination,
            panel="jobs",
            company=company_obj,
        )
    return render_template(
        "company/detail.html", company=company_obj, panel="about", active="detail"
    )


@company.route("/account", methods=["GET", "POST"])
@company_required
def edit():
    form = CompanyDetailForm(obj=current_user)
    logo_url = current_user.logo
    if form.validate_on_submit():
        logo_url = form.update_detail(current_user)
        print(logo_url)
        flash("企业信息更新成功", "success")
    return render_template(
        "company/edit.html", form=form, file_url=logo_url, panel="edit", active="manage"
    )


@company.route("/count")
@company_required
def count():
    delivery = db.session.query(func.count(), Delivery.job_id) \
                        .filter(Delivery.company_id == current_user.get_id())\
                        .group_by(Delivery.job_id)\
                        .all()
    count_data = map(lambda x: {"job_name": get_all_time_job_name(x[1]), "resume_count": x[0]}, delivery)
    count_data = list(count_data)
    count_data_sorted = sorted(count_data, key=lambda e: e.__getitem__('resume_count'), reverse=True)
    job_name_list = []
    job_count_list = []
    for data in count_data_sorted:
        job_name_list.append(data["job_name"])
        job_count_list.append(data["resume_count"])
    return render_template("company/count.html",
                           panel="count",
                           active="manage",
                           job_name_list=job_name_list,
                           job_count_list=job_count_list)


@company.route("/count/job_id")
@company_required
def job_count():
    job_id = request.args.get("job_id", "")
    total = db.session.query(Delivery.job_id)\
                      .filter(Delivery.company_id == current_user.get_id(), Delivery.job_id == job_id)\
                      .count()
    delivery = db.session.query(func.count(), Delivery.status) \
                         .filter(Delivery.company_id == current_user.get_id(), Delivery.job_id == job_id)\
                         .group_by(Delivery.status)\
                         .all()
    data = [] # 总数， 未处理 ， 面试， 不合适
    data.append({"value": total, "name": "总数"})
    for item in delivery:
        if item[1] == 1:
            data.append({"value":item[0], "name": "未处理"})
        elif item[1] == 2:
            data.append({"value": item[0], "name": "面试"})
        elif item[1] == 3:
            data.append({"value": item[0], "name": "不合适"})
    return render_template("company/job_count.html",
                           panel="count",
                           active="manage",
                           data=data,
                           job_name=get_all_time_job_name(job_id))


def get_all_time_job_name(job_id):
    all_time_job_obj = AllTimeJob.query.filter_by(id=job_id).first()
    return all_time_job_obj.name


@company.route("/jobs_manage")
@company_required
def jobs():
    # page = request.args.get("page", default=1, type=int)
    all_time_job = current_user.all_time_job.order_by(AllTimeJob.updated_at.desc())
    part_time_job = current_user.part_time_job.order_by(PartTimeJob.updated_at.desc())
    return render_template(
        "company/jobs.html",
        all_time_jobs=all_time_job,
        part_time_jobs=part_time_job,
        active="manage",
        panel="jobs",
    )


@company.route("/part_time_jobs")
@company_required
def part_time_jobs():
    page = request.args.get("page", default=1, type=int)
    pagination = current_user.part_time_job.order_by(
        PartTimeJob.updated_at.desc()
    ).paginate(page=page, per_page=current_app.config["LIST_PER_PAGE"], error_out=False)
    return render_template(
        "company/jobs.html", pagination=pagination, active="manage", panel="jobs"
    )


@company.route("/resumes")
@company_required
def resumes():
    status = request.args.get("status", "1")
    page = request.args.get("page", default=1, type=int)
    pagination = (
        current_user.delivery.filter_by(status=status)
        .order_by(Delivery.updated_at.desc())
        .paginate(
            page=page, per_page=current_app.config["LIST_PER_PAGE"], error_out=False
        )
    )
    return render_template(
        "company/resumes.html",
        pagination=pagination,
        active="manage",
        panel="resumes",
        status=status,
    )


@company.route("/resume/accept")
@company_required
def resume_accept():
    delivery_id = request.args.get("delivery_id")
    delivery = current_user.delivery.filter_by(id=delivery_id).first_or_404()
    delivery.accept()
    db.session.add(delivery)
    db.session.commit()
    flash("已列入面试", "success")
    return redirect(url_for("company.resumes"))


@company.route("/resume/reject")
@company_required
def resume_reject():
    delivery_id = request.args.get("delivery_id")
    delivery = current_user.delivery.filter_by(id=delivery_id).first_or_404()
    delivery.reject()
    db.session.add(delivery)
    db.session.commit()
    flash("已列入不合适", "warning")
    return redirect(url_for("company.resumes"))


@company.errorhandler(413)
def page_not_found(error):
    flash("图片大小超过限制", "warning")
    return redirect(request.path)


@company.route("/all_companies")
def all_companies():
    companies = MyCompany.query.all()

    return render_template(
        "company/all_companies.html", active="all_companies", companies=companies
    )


@company.route("/search")
def company_search():
    kw = request.args.get("kw")
    if kw is not None and kw != "":
        filter_companies = MyCompany.query.filter(
            MyCompany.name.like("%{}%".format(kw))
        )
        count = filter_companies.count()
        if count != 0:
            return render_template(
                "search.html", filter_companies=filter_companies, name="company"
            )
        else:
            return render_template("company/index.html")
    return render_template("company/index.html")
