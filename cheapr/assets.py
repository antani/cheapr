# -*- coding: utf-8 -*-
from flask.ext.assets import Bundle, Environment

css = Bundle(
    "css/animate.js",
    "libs/bootstrap/dist/css/bootstrap.css",
    "css/style.css",
    "css/revslider.css",
    "css/owl.carousel.css",
    "css/owl.theme.css",
    "css/font-awesome.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.js",
    "js/parallax.js",
    "js/common.js",
    "js/revslider.js",
    "js/owl.carousel.js",
    "js/plugins.js",
    filters='jsmin',
    output="public/js/common_all.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
