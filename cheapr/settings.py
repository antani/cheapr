# -*- coding: utf-8 -*-
import os

os_env = os.environ

class Config(object):
    SECRET_KEY = os_env.get('CHEAPR_SECRET', 'babloo')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://cheapr:cheapr@localhost@5432/cheapr'  # TODO: Change me
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    # Where your media resides
    RESIZE_ROOT = '/home/vantani/cheapr/cheapr/static/cache/media/'

    # The URL where your media is served at. For the best performance you
    # should serve your media with a proper web server, under a subdomain
    # and with cookies turned off.
    RESIZE_URL = '/static/cache/media/'

    # Set to False if you want Flask-Resize to create sub-directories for
    # each resize setting instead of using a hash.
    RESIZE_HASH_FILENAME = True

    # Change if you want to use something other than md5 for your hashes.
    # Supports all methods that hashlib supports.
    RESIZE_HASH_METHOD = 'md5'


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://cheapr:cheapr@localhost:5432/cheapr'  # TODO: Change me
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'memcached'  # Can be "memcached", "redis", etc.
    # Where your media resides
    RESIZE_ROOT = '/home/vantani/cheapr/cheapr/static/cache/media/'
    RESIZE_URL = '/static/cache/media/'
    RESIZE_HASH_FILENAME = True
    RESIZE_HASH_METHOD = 'md5'




class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
