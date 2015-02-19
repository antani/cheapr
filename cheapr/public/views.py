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
import cheapr.mobiles.models
import json
import cheapr.books.models

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
            return render_template("public/book_prices.html", form=form, results=results)
    return render_template("public/home.html", form=form, results=[])

#-----------------------------------------------------------------------------------------------------------------------
@blueprint.route("/mobiles", methods=["GET"])
def mobile_home():
    form = SearchForm(request.form)
    b=cheapr.mobiles.models.Brands()
    best_selling_mobiles=b.flipkart_best_selling_mobiles()
    brands=b.get_all()
    return render_template('public/mobiles_home.html',top_mobiles=[],best_selling_mobiles=best_selling_mobiles,
                           brands=brands,
                           backurl="/mobiles/", form=form)

@blueprint.route('/mobiles/brand/<brand>', methods = ['GET'])
def get_mobile_by_brand(brand=None):
    form = SearchForm(request.form)
    b=cheapr.mobiles.models.Brands()
    mobiles_brand = b.mobile_models_from_brand(brand)
    return render_template('public/brand_mobiles.html', brand=brand, mobiles_brand=mobiles_brand,form=form )

@blueprint.route('/mobiles/<search_item>', methods = ['GET'])
def get_mobile_prices(search_item=None):
    form = SearchForm(request.form)
    r = requests.get('http://localhost:5001/api/1.0/{0}/{1}'.format('mobiles',search_item))
    results = r.json()['results']
    return render_template("public/home.html", form=form, results=results)


@blueprint.route('/mobiles/info/<uuid>', methods = ['GET'])
def get_mobile_info(uuid=None):
    form = SearchForm(request.form)
    blob=requests.get('http://localhost:5001/api/1.0/{0}'.format(uuid))
    if blob:
        json_blob=json.loads(blob.content)
        b=cheapr.mobiles.models.Brands()
        specs=b.get_gsmarena_spec(json_blob['name'])
    else:
        specs=[]
        json_blob=[]

    return render_template('public/mobiles_info.html', blob=json_blob,spec=specs, form=form)

@blueprint.route('/books/info/<uuid>', methods = ['GET'])
def get_books_info(uuid=None):
    form = SearchForm(request.form)
    blob=requests.get('http://localhost:5001/api/1.0/{0}'.format(uuid))
    if blob:
        json_blob=json.loads(blob.content)
        title=json_blob['name']
        #b=cheapr.books.models.GoodReads()
        #goodreads=b.get_goodreads_info(json_blob['name'])
        if title:
            amz=cheapr.books.models.Amazon()
            isbn = amz.amazon_query_isbn(title)
            print uuid,title,isbn
            amazon=amz.amazon_similar_items(isbn)
            amazon_book_details = amazon[0]
        else:
            amazon=amazon_book_details=[]
    else:
        json_blob=[]
        amazon=[]
        amazon_book_details=[]
        goodreads=[]

    return render_template('public/books_info.html',
                           blob=json_blob, goodreads=[],amazon=amazon[1:],
                           amazon_book_details=amazon_book_details,
                           form=form)
#-----------------------------------------------------------------------------------------------------------------------

@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
