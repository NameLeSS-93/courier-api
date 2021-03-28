from datetime import datetime

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from courier_api import db, app


class Courier(db.Model):
    courier_id = db.Column(db.Integer, primary_key=True)
    courier_type = db.Column(db.String(10), nullable=False)
    regions = db.Column(postgresql.ARRAY(db.Integer,
                                         dimensions=1), nullable=False)
    working_hours = db.Column(postgresql.ARRAY(db.String(15),
                                               dimensions=1), nullable=False)
    capacity = db.Column(db.Float, nullable=False)
    child = relationship("Order", backref="courier", cascade="all,delete")

    def __repr__(self):
        return f'courier_id: {self.courier_id}, courier_type: {self.courier_type}'


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    region = db.Column(db.Integer, nullable=False)
    delivery_hours = db.Column(postgresql.ARRAY(db.String(15),
                                                dimensions=1), nullable=False)
    courier_id = db.Column(db.Integer,
                           db.ForeignKey('courier.courier_id', ondelete='CASCADE'))
    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())
    delivery_way = db.Column(db.String(4))
    status = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'order_id: {self.order_id}, w: {self.weight}, ' \
               f'region: {self.region}'
