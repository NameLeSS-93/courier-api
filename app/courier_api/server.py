import re
import functools
import logging
from datetime import datetime

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from flask import request, jsonify
from sqlalchemy import func
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from .schema_validators import courier_post_schema, order_post_schema,\
                              data_schema, assign_post_schema,\
                              complete_post_schema
from .models import Courier, Order
from courier_api import app, db


logging.basicConfig(filename='./logs/app.log', level=logging.INFO, format='%(asctime)s \
    %(levelname)s | %(message)s')


capacity = {
    'foot': 10,
    'bike': 15,
    'car': 50
}

pay_coeff = {
    'foot': 2,
    'bike': 5,
    'car': 9
}


def json_req_read(fnc):
    @functools.wraps(fnc)
    def check(*args, **kwargs):
        try:
            return fnc(*args, **kwargs)
        except BadRequest:
            logging.warning('Request body is not a valid JSON')
            return jsonify(error='Request body is not a valid JSON'), 400
    return check


def check_intersect(l_1, l_2):
    l_1.sort()
    l_2.sort()
    count = max(len(l_1), len(l_2))
    for i in l_1:
        if i[1] == 0:
            i[1] = 2400

    for i in l_2:
        if i[1] == 0:
            i[1] = 2400
    i, j = 0, 0
    while count:
        try:
            if l_1[i][0] < l_2[j][1] and l_1[i][1] > l_2[j][0]:
                return True
            elif l_1[i][1] <= l_2[j][0]:
                i += 1
            elif l_2[j][1] <= l_1[i][0]:
                j += 1
            count -= 1
        except IndexError:
            break
    return False


def str_to_int(lst):
    return [int(k) for k in lst.replace(':', '').split('-')]


def json_valid(e, data, num=None):
    suffix = {
        1: 'st',
        2: 'nd',
        3: 'rd',
        4: 'th'
    }
    if num > 4:
        suf_num = 4
    else:
        suf_num = num
    wrong_key = re.findall('(\'.+\') is a required property', e.__str__())
    if not wrong_key:
        wrong_type = e.__str__().split('\n')[0].split("'")[-2]
        key = e.__str__().split('\n')[-2].split("'")
        error = f'Key \'{key[1]}\' should be {wrong_type} ' \
                             f'type. {type(data[key[1]]).__name__} ' \
                             f'was given in {num}{suffix[suf_num]} data set'
        logging.warning(error)
        return {'error': error}
    logging.warning(f'{str(*wrong_key)} key required in {num}{suffix[suf_num]} set of data')
    return {'error' : f'{str(*wrong_key)} key required in ' \
                         f'{num}{suffix[suf_num]} set of data'}


@app.route('/couriers', methods=['POST'])
@json_req_read
def couriers():
    data = request.get_json()
    try:
        validate(data, schema=data_schema)
    except ValidationError as e:
        wrong_key = re.findall('(\'.+\') is a required property', e.__str__())
        logging.warning(str(*wrong_key) + ' key is required')
        return jsonify(error=str(*wrong_key) + ' key is required'), 400
    added = []
    err = []
    for num, courier in enumerate(data['data'], start=1):
        try:
            validate(courier, schema=courier_post_schema)
        except ValidationError as e:
            res = json_valid(e, courier, num)
            return jsonify(res), 400
        try:
            cour = Courier(courier_id=courier['courier_id'],
                           courier_type=courier['courier_type'],
                           regions=courier['regions'],
                           working_hours=courier['working_hours'],
                           capacity=capacity[courier['courier_type']]
                           )
            db.session.add(cour)

            # TODO add accurate exception
        except:
            err.append({'id': courier['courier_id']})
        added.append({'id': courier['courier_id']})
    try:
        db.session.commit()
        # logging.info(f'Couriers {added} added to db')
    except (IntegrityError, UniqueViolation) as e:
        if 'UniqueViolation' in e.args[0]:
            non_unique_key = re.findall('Key (\(.+\)=\(.+\))',
                                        e.args[0])[0]
            logging.warning(f'{non_unique_key} ' \
                            f'is already in the database')
            return jsonify(error=f'{non_unique_key} '
                                 f'is already in the database'), 400
        logging.warning(str(e.args[0]))
        return jsonify(error=e.args[0]), 400
    if len(err):
        logging.warning(f'{err} were not added to db')
        return jsonify(validation_error={'couriers': err}), 400
    logging.info(f'Courier(s) {added} successfully added to db')
    return jsonify(couriers=added), 201


@app.route('/orders', methods=['POST'])
@json_req_read
def orders():
    data = request.get_json()
    try:
        validate(data, schema=data_schema)
    except ValidationError as e:
        wrong_key = re.findall('(\'.+\') is a required property', e.__str__())
        return jsonify(error=str(*wrong_key) + ' key is required'), 400
    added = []
    err = []
    for num, order in enumerate(data['data'], start=1):
        try:
            validate(order, schema=order_post_schema)
        except ValidationError as e:
            res = json_valid(e, order, num)
            return jsonify(res), 400
        try:
            new_order = Order(order_id=order['order_id'],
                              weight=order['weight'],
                              region=order['region'],
                              delivery_hours=order['delivery_hours'])

            db.session.add(new_order)
        # TODO add accurate exception
        except Exception as e:
            err.append({'id': order['order_id']})
        added.append({'id': order['order_id']})
    try:
        db.session.commit()
    except (IntegrityError, UniqueViolation) as e:
        if 'UniqueViolation' in e.args[0]:
            non_unique_key = re.findall('Key (\(.+\)=\(.+\))',
                                        e.args[0])[0]
            return jsonify(error=f'{non_unique_key} is already '
                                 f'in the database'), 400
        return jsonify(error='Data cannot be added in '
                             'database'), 400
    if len(err):
        return jsonify(validation_error={'orders': err}), 400
    return jsonify(orders=added), 201


@app.route('/orders/assign', methods=['POST'])
@json_req_read
def assign():
    data = request.get_json()
    try:
        validate(data, schema=assign_post_schema)
    except ValidationError as e:
        wrong_key = re.findall('(\'.+\') is a required property', e.__str__())
        if wrong_key:
            return jsonify(error=str(*wrong_key) + ' key is required'), 400
        else:
            wrong_type = e.__str__().split('\n')[0].split("'")[-2]
            key = e.__str__().split('\n')[-2].split("'")
            return jsonify(error=f'Key \'{key[1]}\' should be {wrong_type} '\
                                 f'type. {type(data[key[1]]).__name__} '\
                                 f'was given.'), 400
    courier_id = data['courier_id']
    courier = Courier.query.filter_by(courier_id=courier_id).first()
    if not courier:
        return jsonify(error='Wrong courier_id'), 400

    cour_capacity = courier.capacity
    available_orders = Order.query.filter_by(
        status=0).order_by(Order.weight).all()
    out_order_id = []

    for order in available_orders:
        if order.region in courier.regions:
            cour_int = []
            for i in courier.working_hours:
                tup = str_to_int(i)
                cour_int.append(tup)
            order_int = []
            for i in order.delivery_hours:
                tup = str_to_int(i)
                order_int.append(tup)
            if check_intersect(cour_int, order_int)\
                    and (cour_capacity - order.weight) >= 0:
                cour_capacity -= order.weight
                d = datetime.now()
                order.query.filter_by(order_id=order.order_id)\
                    .update({'status': 1, 'start_time': d,
                             'courier_id': courier_id})
                courier.query.filter_by(courier_id=courier_id)\
                    .update({'capacity': cour_capacity})
                db.session.commit()
                out_order_id.append({'id': order.order_id})
    if out_order_id:
        return jsonify(orders=sorted(out_order_id, key=lambda x: x['id']),
                       assign_time=d.isoformat('T')[:-4] + 'Z')
    else:
        return jsonify(orders=[])


@app.route('/orders/complete', methods=['POST'])
@json_req_read
def complete():
    data = request.get_json()
    try:
        validate(data, schema=complete_post_schema)
    except ValidationError as e:
        wrong_key = re.findall('(\'.+\') is a required property', e.__str__())
        if wrong_key:
            return jsonify(error=str(*wrong_key) + ' key is required'), 400
        else:
            wrong_type = e.__str__().split('\n')[0].split("'")[-2]
            key = e.__str__().split('\n')[-2].split("'")
            return jsonify(error=f'Key \'{key[1]}\' should be {wrong_type} '\
                                 f'type. {type(data[key[1]]).__name__} '\
                                 f'was given.'), 400
    try:
        courier_id = data['courier_id']
        order_id = data['order_id']
        complete_time = data['complete_time']
    except KeyError as e:
        return jsonify(error=f'Error key name {e.__str__()}')

    courier = Courier.query.filter_by(courier_id=courier_id).first()
    order = Order.query.filter_by(courier_id=courier_id,
                                  order_id=order_id).first()

    if order and order.status == 1:
        order.query.filter_by(order_id=order_id) \
            .update({'status': 2, 'end_time': complete_time,
                     'delivery_way': courier.courier_type})
        courier.query.filter_by(courier_id=courier_id) \
            .update({'capacity': courier.capacity + order.weight})
        db.session.commit()
        return jsonify(order_id=order_id)
    else:
        return jsonify(error='No order or courier found'), 400


@app.route('/couriers/<int:courier_id>', methods=['GET', 'PATCH'])
@json_req_read
def courier_stat(courier_id):
    if request.method == 'GET':
        courier = Courier.query.filter_by(courier_id=courier_id).first()
        if not courier:
            return jsonify(error=f'No courier with courier_id {courier_id}'), \
                400
        courier_regions = courier.regions
        finished_orders = Order.query.filter_by(courier_id=courier_id,
                                                status=2).all()
        num_finished = len(finished_orders)
        if num_finished == 0:
            return jsonify(courier_id=courier_id,
                           courier_type=courier.courier_type,
                           regions=courier.regions,
                           working_hours=courier.working_hours,
                           earnings=0)

        delivery_ways = db.session.query(Order.delivery_way,
                                         func.count(Order.delivery_way) \
                                         .label('count')).filter(
            Order.courier_id == courier_id, Order.status == 2) \
            .group_by(Order.delivery_way).all()

        avg_regions_time = []
        for region in courier_regions:
            avg_region_time = []
            finished_orders = Order.query.filter_by(region=region,
                                                    status=2,
                                                    courier_id=courier_id) \
                                                    .order_by(Order.end_time) \
                                                    .all()
            for num, ord_id in enumerate(finished_orders):
                if num == 0:
                    start_time = ord_id.start_time
                end_time = ord_id.end_time
                avg_region_time.append((end_time - start_time).seconds)
                start_time = end_time

            if avg_region_time:
                avg = sum(avg_region_time) / len(avg_region_time)
                avg_regions_time.append(avg)
        earnings = 0
        try:
            min_delivery_time = min(avg_regions_time)
            rating = (3600 - min(min_delivery_time, 3600)) / 3600 * 5
            for i in delivery_ways:
                earnings += pay_coeff[i[0]] * 500 * i[1]
            return jsonify(courier_id=courier_id,
                           courier_type=courier.courier_type,
                           regions=courier.regions,
                           working_hours=courier.working_hours,
                           rating=round(rating, 2),
                           earnings=earnings)
        except ValueError:
            return jsonify(courier_id=courier_id,
                           courier_type=courier.courier_type,
                           regions=courier.regions,
                           working_hours=courier.working_hours,
                           earnings=earnings)
    elif request.method == 'PATCH':
        courier_before = Courier.query.filter_by(
            courier_id=courier_id).first()
        if not courier_before:
            return jsonify(error=f'No courier with courier_id {courier_id}'), \
                400
        type_before = courier_before.courier_type
        capacity_before = courier_before.capacity
        data = request.get_json()
        try:
            Courier.query.filter_by(courier_id=courier_id).update(data)
            db.session.commit()
        except:
            return jsonify(error='Check if JSON keys ' \
                                 'are spelled correctly'), 400
        courier_after = Courier.query.filter_by(courier_id=courier_id).first()
        if 'working_hours' in data.keys() or 'courier_type' in data.keys():
            if capacity[type_before] > capacity[courier_after.courier_type]:
                carried_weight = capacity[type_before] - capacity_before
                over_weight = capacity[courier_after.courier_type] \
                    - carried_weight
                if over_weight < 0:
                    in_delivery = Order.query.filter_by(courier_id=courier_id,
                                                        status=1).order_by(
                        Order.weight.desc()).all()
                    for order in in_delivery:
                        Order.query.filter_by(
                            order_id=order.order_id) \
                            .update({'status': 0, 'courier_id': None})
                        over_weight += order.weight
                        Courier.query.filter_by(
                            courier_id=courier_id) \
                            .update({'capacity': over_weight})
                        db.session.commit()
                        if over_weight >= 0:
                            break
            in_delivery = Order.query.filter_by(
                courier_id=courier_id, status=1).all()
            for order in in_delivery:
                ord_time = []
                cour_time = []
                for time in order.delivery_hours:
                    ord_time.append(str_to_int(time))
                for time in courier_after.working_hours:
                    cour_time.append(str_to_int(time))
                if not check_intersect(ord_time, cour_time):
                    over_weight += order.weight
                    Courier.query.filter_by(
                        courier_id=courier_id) \
                        .update({'capacity': over_weight})
                    Order.query.filter_by(
                        order_id=order.order_id) \
                        .update({'status': 0, 'courier_id': None})
                    db.session.commit()
        return jsonify(courier_id=courier_after.courier_id,
                       courier_type=courier_after.courier_type,
                       regions=courier_after.regions,
                       working_hours=courier_after.working_hours)

# for test purposes only !!!
@app.route('/couriers/delete/<int:courier_id>', methods=['DELETE'])
def courier_delete(courier_id):
    q = Courier.query.filter_by(courier_id=courier_id).first()
    if q:
        db.session.delete(q)
        db.session.commit()
        return jsonify(courier_id=courier_id), 200
    return jsonify(error=f'Wrong courier_id'), 400


@app.route('/orders/delete/<int:order_id>', methods=['DELETE'])
def order_delete(order_id):
    q = Order.query.filter_by(order_id=order_id).first()
    if q:
        db.session.delete(q)
        db.session.commit()
        return jsonify(order_id=order_id), 200
    return jsonify(error=f'Wrong order_id'), 400

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
