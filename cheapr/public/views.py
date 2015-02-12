# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_user, login_required, logout_user

from cheapr.extensions import login_manager
from cheapr.user.models import User
from cheapr.public.forms import SearchForm
from cheapr.user.forms import RegisterForm
from cheapr.utils import flash_errors
from cheapr.database import db
import requests
import logging
import datetime
from flask import request

LOG_FILENAME = 'cheapr_access_log.log'
info_log = logging.getLogger('app_info_log')
info_log.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=1024 * 1024 * 100,
    backupCount=20
    )

info_log.addHandler(handler)
blueprint = Blueprint('public', __name__, static_folder="../static")

@blueprint.before_request
def pre_request_logging():
    #Logging statement
    if 'text/html' in request.headers['Accept']:
        info_log.info('\t'.join([
            datetime.datetime.today().ctime(),
            request.remote_addr,
            request.method,
            request.url,
            request.data,
            ', '.join([': '.join(x) for x in request.args]),
            ', '.join([': '.join(x) for x in request.headers])])
        )




@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = SearchForm(request.form)
    print form.searchterm.data
    print form.searchtype.data
    # Handle logging in
    if request.method == 'POST':
        if not form.validate_on_submit():
            print "not validated"
            flash_errors(form)
            # login_user(form.user)
            # flash("You are logged in.", 'success')
            # redirect_url = request.args.get("next") or url_for("user.members")
            # return redirect(redirect_url)
            return redirect(url_for('public.home'))
        else:
            print "validated"
            r = requests.get('http://localhost:5001/api/1.0/{0}/{1}'.format(form.searchtype.data,form.searchterm.data))
            results = r.json()['results']
            return render_template("public/home.html", form=form, results=results)
    return render_template("public/home.html", form=form, results=[])

@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))

@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        active=True)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)

@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
