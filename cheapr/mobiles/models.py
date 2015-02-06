__author__ = 'vantani'
from database import (db,Model)
from sqlalchemy.dialects.postgresql import JSON

class MobileBrand(Model):
    __tablename__ = 'mobile_brands'
    id=db.Column(db.Integer,primary_key=True)
    img=db.Column(db.String(1024), nullable=True)
    name=db.Column(db.String(200), nullable=True)
    link=db.Column(db.String(1024), nullable=True)
    top_brand = db.Column(db.Integer, nullable=False)

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<MobileBrand({name})>'.format(name=self.name)


class MobileModel(Model):
    __tablename__ = 'mobile_models'
    id=db.Column(db.Integer,primary_key=True)
    img=db.Column(db.String(1024), nullable=True)
    name=db.Column(db.String(400), nullable=True)
    canonical_name=db.Column(db.String(1024), nullable=True)
    description=db.Column(db.String(1024), nullable=True)
    url=db.Column(db.String(1024), nullable=True)
    maker=db.Column(db.String(256), nullable=True)
    fields=db.Column(JSON)
    top_mobile = db.Column(db.Integer, nullable=False)

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<MobileModel({name})>'.format(name=self.name)
