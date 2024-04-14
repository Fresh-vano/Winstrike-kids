from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Element(db.Model):
    __tablename__ = 'elements'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    manufacturer = db.Column(db.String(128))
    analysis_date_time = db.Column(db.DateTime, default=datetime.utcnow)
    file_name = db.Column(db.String(256))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Text)

    category = db.relationship('Category', back_populates='elements')
    characteristics = db.relationship('ElementCharacteristic', back_populates='element', cascade="all, delete")

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    energy_value_min = db.Column(db.Float)
    energy_value_max = db.Column(db.Float)
    sodium_min = db.Column(db.Float)
    sodium_max = db.Column(db.Float)
    total_sugar_min = db.Column(db.Float)
    total_sugar_max = db.Column(db.Float)
    free_sugars_min = db.Column(db.Float)
    free_sugars_max = db.Column(db.Float)
    total_protein_min = db.Column(db.Float)
    total_protein_max = db.Column(db.Float)
    total_fat_min = db.Column(db.Float)
    total_fat_max = db.Column(db.Float)
    fruit_content_min = db.Column(db.Float)
    fruit_content_max = db.Column(db.Float)
    age_marking_min = db.Column(db.Float)
    age_marking_max = db.Column(db.Float)
    high_sugar_front_packaging_min = db.Column(db.Float)
    high_sugar_front_packaging_max = db.Column(db.Float)
    labeling_requirements = db.Column(db.Boolean)

    elements = db.relationship('Element', back_populates='category')

class ElementCharacteristic(db.Model):
    __tablename__ = 'element_characteristics'

    id = db.Column(db.Integer, primary_key=True)
    element_id = db.Column(db.Integer, db.ForeignKey('elements.id'), nullable=False)
    energy_value = db.Column(db.Float)
    sodium = db.Column(db.Float)
    total_sugar = db.Column(db.Float)
    free_sugars = db.Column(db.Float)
    total_protein = db.Column(db.Float)
    total_fat = db.Column(db.Float)
    fruit_content = db.Column(db.Float)
    age_marking = db.Column(db.Float)
    high_sugar_front_packaging = db.Column(db.Float)
    labeling = db.Column(db.Boolean)

    element = db.relationship('Element', back_populates='characteristics')

class AnalysisLog(db.Model):
    __tablename__ = 'analysis_logs'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.String(512))
    element_id = db.Column(db.Integer, db.ForeignKey('elements.id'), nullable=True)

    element = db.relationship('Element', backref='analysis_logs')