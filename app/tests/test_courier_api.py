import random
from datetime import datetime, timedelta

import pytest
import requests


# for TestCouriersPost
id =  random.sample(range(100, 1000), 3)
cour_types = ['foot', 'bike', 'car']
random.shuffle(cour_types)
regions = []
HOST = '0.0.0.0'
PORT = '8080'
# print(cour_type)
for i in range(3):
    arr = random.sample(range(1, 50), random.randint(1, 10))
    # print(arr)
    regions.append(arr)

# for TestPostOrders

rand_weights = []
regions_order = []
for i in range(3):
    rand_weights.append(random.randint(1, 17))
    regions_order.append(random.randint(1, 50))

COURIER_ID = 9999
ORDER_ID = 9999

couriers = []
orders = []

class TestCouriersPost:
    global couriers
    def test_couriers_201(self):
        req_body = {
            "data": [
                {
                    "courier_id": id[0],
                    "courier_type": cour_types[0],
                    "regions": regions[0],
                    "working_hours": [
                        "11:35-14:05",
                        "09:00-11:00"
                    ]
                },
                {
                    "courier_id": id[1],
                    "courier_type": cour_types[1],
                    "regions": regions[1],
                    "working_hours": [
                        "09:00-18:00"
                    ]
                },
                {
                    "courier_id": id[2],
                    "courier_type": cour_types[2],
                    "regions": regions[2],
                    "working_hours": []
                }
            ]
        }
        res = requests.post(f'http://{HOST}:{PORT}/couriers', json=req_body)
        # import  pdb; pdb.set_trace()
        assert "couriers" in res.json()
        for i, j in zip(res.json()['couriers'], req_body['data']):
            # print(i, j)
            assert i['id'] == j['courier_id']
        assert res.status_code == 201
        for i in id:
            couriers.append(i)

    def test_couriers_400(self):
        req_body = {
            "data": [
                {
                    "courier_id": id[0],
                    "courier_type": cour_types[0],
                    "regions": regions[0],
                    "working_hours": [
                        "11:35-14:05",
                        "09:00-11:00"
                    ]
                },
                {
                    "courier_id": id[1],
                    "courier_type": cour_types[1],
                    "regions": regions[1],
                    "working_hours": [
                        "09:00-18:00"
                    ]
                },
                {
                    "courier_id": id[2],
                    "courier_type": cour_types[2],
                    "regions": regions[2],
                    "working_hours": []
                }
            ]
        }
        res = requests.post(f'http://{HOST}:{PORT}/couriers', json=req_body)
        assert res.status_code == 400

    def test_wrong_data_key(self):
        id_1 = 101
        id_2 = 102

        req_body = {
            "dat": [
                {
                    "courier_id": id_1,
                    "courier_type": cour_types[0],
                    "regions": regions[1],
                    "working_hours": [
                        "11:35-14:05",
                        "09:00-11:00"
                    ]
                },
                {
                    "courier_id": id_2,
                    "type": cour_types[1],
                    "regions": regions[1],
                    "working_hours": [
                        "09:00-18:00"
                    ]
                }
            ]
        }
        res = requests.post(f'http://{HOST}:{PORT}/couriers', json=req_body)
        assert res.status_code == 400
        assert res.json()['error'] == "'data' key is required"
        # couriers.append(id_1)
        # couriers.append(id_2)


    def test_fake_key_cour(self):
        req_body = {
            "data": [
                {
                    "courier_id": random.randint(1001, 1100),
                    "courier_type": cour_types[0],
                    "regions": regions[1],
                    "working_hours": [
                        "11:35-14:05",
                        "09:00-11:00"
                    ]
                },
                {
                    "courier_id": random.randint(1001, 1100),
                    "type": cour_types[1],
                    "regions": regions[1],
                    "working_hours": [
                        "09:00-18:00"
                    ]
                }
            ]
        }
        res = requests.post(f'http://{HOST}:{PORT}/couriers', json=req_body)
        assert res.status_code == 400
        assert res.json()['error'] == "'courier_type' key required in 2nd set of data"

    def test_wrong_value_type(self):
        req_body = {
            "data": [
                {
                    "courier_id": random.randint(1001, 1100),
                    "courier_type": cour_types[0],
                    "regions": regions[1],
                    "working_hours": [
                        "11:35-14:05",
                        "09:00-11:00"
                    ]
                },
                {
                    "courier_id": str(random.randint(1001, 1100)),
                    "courier_type": cour_types[1],
                    "regions": regions[1],
                    "working_hours": [
                        "09:00-18:00"
                    ]
                }
            ]
        }
        res = requests.post(f'http://{HOST}:{PORT}/couriers', json=req_body)
        assert res.status_code == 400
        assert res.json()['error'] == "Key 'courier_id' should be number type. str was given in 2nd data set"



class TestPostOrders:
    global orders
    def test_orders_201(self):
        req_body = {
            "data": [
                {
                    "order_id": id[0],
                    "weight": rand_weights[0],
                    "region": regions_order[0],
                    "delivery_hours": [
                        "11:35-14:05",
                        "09:00-11:00"
                    ]
                },
                {
                    "order_id": id[1],
                    "weight": rand_weights[1],
                    "region": regions_order[1],
                    "delivery_hours": [
                        "09:00-18:00"
                    ]
                },
                {
                    "order_id": id[2],
                    "weight": rand_weights[2],
                    "region": regions_order[2],
                    "delivery_hours": []
                }
            ]
        }
        res = requests.post(f'http://{HOST}:{PORT}/orders', json=req_body)
        assert "orders" in res.json()
        for i, j in zip(res.json()['orders'], req_body['data']):
            # print(i, j)
            assert i['id'] == j['order_id']
        assert res.status_code == 201
        for i in id:
            orders.append(i)

    def test_orders_400(self):
        req_body = {
            "data": [
                {
                    "order_id": id[0],
                    "weight": rand_weights[0],
                    "region": regions_order[0],
                    "delivery_hours": [
                        "11:35-14:05",
                        "09:00-11:00"
                    ]
                },
                {
                    "order_id": id[1],
                    "weight": rand_weights[1],
                    "region": regions_order[1],
                    "delivery_hours": [
                        "09:00-18:00"
                    ]
                },
                {
                    "order_id": id[2],
                    "weight": rand_weights[2],
                    "region": regions_order[2],
                    "delivery_hours": []
                }
            ]
        }
        res = requests.post(f'http://{HOST}:{PORT}/orders', json=req_body)
        assert res.status_code == 400

    def test_wrong_data_key(self):
        req_body = {
            "daa": [
                {
                    "order_id": id[0],
                    "weight": rand_weights[0],
                    "region": regions_order[0],
                    "delivery_hours": [
                        "11:35-14:05",
                        "09:00-11:00"
                    ]
                },
                {
                    "order_id": id[1],
                    "weight": rand_weights[1],
                    "region": regions_order[1],
                    "delivery_hours": [
                        "09:00-18:00"
                    ]
                },
                {
                    "order_id": id[2],
                    "weight": rand_weights[2],
                    "region": regions_order[2],
                    "delivery_hours": []
                }
            ]
        }
        res = requests.post(f'http://{HOST}:{PORT}/orders', json=req_body)
        assert res.status_code == 400
        assert res.json()['error'] == "'data' key is required"


    def test_fake_key(self):
        req_body = {
            "data": [
                {
                    "ordr_id": id[0],
                    "weight": rand_weights[0],
                    "region": regions_order[0],
                    "delivery_hours": [
                        "11:35-14:05",
                        "09:00-11:00"
                    ]
                },
                {
                    "order_id": id[1],
                    "weight": rand_weights[1],
                    "region": regions_order[1],
                    "delivery_hours": [
                        "09:00-18:00"
                    ]
                },
                {
                    "order_id": id[2],
                    "weight": rand_weights[2],
                    "region": regions_order[2],
                    "delivery_hours": []
                }
            ]
        }
        res = requests.post(f'http://{HOST}:{PORT}/orders', json=req_body)
        assert res.status_code == 400
        assert res.json()['error'] == "'order_id' key required in 1st set of data"

    def test_wrong_value_type(self):
        req_body = {
            "data": [
                {
                    "order_id": id[0],
                    "weight": rand_weights[0],
                    "region": regions_order[0],
                    "delivery_hours": [
                        "11:35-14:05",
                        "09:00-11:00"
                    ]
                },
                {
                    "order_id": id[1],
                    "weight": rand_weights[1],
                    "region": regions_order[1],
                    "delivery_hours": [
                        "09:00-18:00"
                    ]
                },
                {
                    "order_id": id[2],
                    "weight": rand_weights[2],
                    "region": str(regions_order[2]),
                    "delivery_hours": []
                }
            ]
        }
        res = requests.post(f'http://{HOST}:{PORT}/orders', json=req_body)
        assert res.status_code == 400
        assert res.json()['error'] == "Key 'region' should be number type. str was given in 3rd data set"

class TestAssign:
    global couriers
    global orders
    def test_assign_suitable_order(self):

        global ORDER_ID
        global COURIER_ID

        courier = {
            "data": [
                {
                    "courier_id": COURIER_ID,
                    "courier_type": "foot",
                    "regions": [10],
                    "working_hours": [
                        "20:35-21:35",
                        "22:00-00:00"
                    ]
                }
            ]
        }
        order = {
            "data": [
                {
                    "order_id": ORDER_ID,
                    "weight": 9,
                    "region": 10,
                    "delivery_hours": [
                        "21:00-00:00"
                    ]
                }
            ]
        }
        assign = {
	       "courier_id": COURIER_ID
        }

        res_cour = requests.post(f'http://{HOST}:{PORT}/couriers', json=courier)
        res_order = requests.post(f'http://{HOST}:{PORT}/orders', json=order)
        res_assign = requests.post(f'http://{HOST}:{PORT}/orders/assign', json=assign)

        assert res_assign.status_code == 200
        assert res_assign.json()['orders'][0]['id'] == ORDER_ID
        couriers.append(COURIER_ID)
        orders.append(ORDER_ID)
        COURIER_ID += 1
        ORDER_ID += 1

    def test_too_heavy_order(self):

        global ORDER_ID
        global COURIER_ID

        courier = {
            "data": [
                {
                    "courier_id": COURIER_ID,
                    "courier_type": "foot",
                    "regions": [10],
                    "working_hours": [
                        "20:35-21:35",
                        "22:00-00:00"
                    ]
                }
            ]
        }
        order = {
            "data": [
                {
                    "order_id": ORDER_ID,
                    "weight": 11,
                    "region": 10,
                    "delivery_hours": [
                        "21:00-00:00"
                    ]
                }
            ]
        }
        assign = {
	       "courier_id": COURIER_ID
        }
        res_cour = requests.post(f'http://{HOST}:{PORT}/couriers', json=courier)
        res_order = requests.post(f'http://{HOST}:{PORT}/orders', json=order)
        res_assign = requests.post(f'http://{HOST}:{PORT}/orders/assign', json=assign)

        assert res_assign.status_code == 200
        assert res_assign.json()['orders'] == []
        couriers.append(COURIER_ID)
        orders.append(ORDER_ID)
        COURIER_ID += 1
        ORDER_ID += 1


    def test_other_region_order(self):

        global ORDER_ID
        global COURIER_ID

        courier = {
            "data": [
                {
                    "courier_id": COURIER_ID,
                    "courier_type": "foot",
                    "regions": [10],
                    "working_hours": [
                        "20:35-21:35",
                        "22:00-00:00"
                    ]
                }
            ]
        }
        order = {
            "data": [
                {
                    "order_id": ORDER_ID,
                    "weight": 1,
                    "region": 11,
                    "delivery_hours": [
                        "21:00-00:00"
                    ]
                }
            ]
        }
        assign = {
           "courier_id": COURIER_ID
        }
        res_cour = requests.post(f'http://{HOST}:{PORT}/couriers', json=courier)
        res_order = requests.post(f'http://{HOST}:{PORT}/orders', json=order)
        res_assign = requests.post(f'http://{HOST}:{PORT}/orders/assign', json=assign)

        assert res_assign.status_code == 200
        assert res_assign.json()['orders'] == []
        couriers.append(COURIER_ID)
        orders.append(ORDER_ID)
        COURIER_ID += 1
        ORDER_ID += 1

    def test_other_hours_order(self):

        global ORDER_ID
        global COURIER_ID

        courier = {
            "data": [
                {
                    "courier_id": COURIER_ID,
                    "courier_type": "foot",
                    "regions": [10],
                    "working_hours": [
                        "14:00-18:00"
                    ]
                }
            ]
        }
        order = {
            "data": [
                {
                    "order_id": ORDER_ID,
                    "weight": 1,
                    "region": 10,
                    "delivery_hours": [
                        "12:00-14:00",
                        "18:00-00:00"
                    ]
                }
            ]
        }
        assign = {
           "courier_id": COURIER_ID
        }
        res_cour = requests.post(f'http://{HOST}:{PORT}/couriers', json=courier)
        res_order = requests.post(f'http://{HOST}:{PORT}/orders', json=order)
        res_assign = requests.post(f'http://{HOST}:{PORT}/orders/assign', json=assign)
        couriers.append(COURIER_ID)
        orders.append(ORDER_ID)
        assert res_assign.status_code == 200
        assert res_assign.json()['orders'] == []

        COURIER_ID += 1
        ORDER_ID += 1

    def test_wrong_courier_id(self):

        assign = {
           "courier_id": 0
        }
        res_assign = requests.post(f'http://{HOST}:{PORT}/orders/assign', json=assign)

        assert res_assign.status_code == 400
        assert res_assign.json()['error'] == "Wrong courier_id"


class TestComlete:
    global couriers
    global orders
    def test_complete(self):

        global ORDER_ID
        global COURIER_ID

        courier = {
            "data": [
                {
                    "courier_id": 111,
                    "courier_type": "foot",
                    "regions": [10, 11, 12],
                    "working_hours": [
                        "14:00-19:00"
                    ]
                }
            ]
        }
        order = {
            "data": [
                {
                    "order_id": ORDER_ID,
                    "weight": 1,
                    "region": 10,
                    "delivery_hours": [
                        "12:00-14:00",
                        "18:00-00:00"
                    ]
                }
            ]
        }
        assign = {
           "courier_id": 111
        }

        res_cour = requests.post(f'http://{HOST}:{PORT}/couriers', json=courier)
        res_order = requests.post(f'http://{HOST}:{PORT}/orders', json=order)
        res_assign = requests.post(f'http://{HOST}:{PORT}/orders/assign', json=assign)
        time_now = datetime.now()
        complete_time = time_now + timedelta(0,900)

        complete = {
            "courier_id": 111,
            "order_id": ORDER_ID,
            "complete_time": f"{complete_time.isoformat('T')[:-4]}Z"
        }
        res_complete = requests.post(f'http://{HOST}:{PORT}/orders/complete', json=complete)
        assert res_complete.status_code == 200
        assert res_complete.json()['order_id'] == ORDER_ID
        couriers.append(111)
        orders.append(ORDER_ID)
        COURIER_ID += 1
        ORDER_ID += 1

    def test_complete_wrong_order_courier_ids(self):

        global ORDER_ID
        global COURIER_ID

        time_now = datetime.now()
        complete_time = time_now + timedelta(0,900)

        complete = {
            "courier_id": COURIER_ID,
            "order_id": ORDER_ID,
            "complete_time": f"{complete_time.isoformat('T')[:-4]}Z"
        }
        res_complete = requests.post(f'http://{HOST}:{PORT}/orders/complete', json=complete)
        assert res_complete.status_code == 400
        assert res_complete.json()['error'] == 'No order or courier found'
        # COURIER_ID += 1
        # ORDER_ID += 1

class TestCourierGet:
    def test_courier_get(self):
        global COURIER_ID

        res_get = requests.get(f'http://{HOST}:{PORT}/couriers/111')
        assert res_get.status_code == 200
        assert res_get.json()["rating"] == (3600 - 900) / 3600 * 5
        assert res_get.json()["earnings"] == 2 * 500

    def test_courier_no_finished_orders(self):

        global COURIER_ID
        global ORDER_ID

        res_get = requests.get(f'http://{HOST}:{PORT}/couriers/{COURIER_ID - 2}')
        assert res_get.status_code == 200
        assert res_get.json().get("rating") == None
        assert res_get.json()["earnings"] == 0
        COURIER_ID += 1
        ORDER_ID += 1

class TestCourierPatch:
    global couriers
    global orders
    def test_change_courier(self):

        global COURIER_ID
        global ORDER_ID

        courier = {
            "data": [
                {
                    "courier_id": COURIER_ID,
                    "courier_type": "foot",
                    "regions": [10, 11, 12],
                    "working_hours": [
                        "14:00-19:00"
                    ]
                }
            ]
        }
        patch = {
            "courier_type": "bike",
            "regions": [9, 10, 11, 12],
            "working_hours": ["12:00-19:00", "20:00-00:00"]
        }
        res_post = requests.post(f'http://{HOST}:{PORT}/couriers', json=courier)
        res_patch = requests.patch(f'http://{HOST}:{PORT}/couriers/{COURIER_ID}', json=patch)
        assert res_patch.json()['courier_type'] == 'bike'
        assert res_patch.json()['regions'] == [9, 10, 11, 12]
        assert res_patch.json()['working_hours'] == ["12:00-19:00", "20:00-00:00"]
        couriers.append(COURIER_ID)
        # orders.append(ORDER_ID)
        COURIER_ID += 1
        ORDER_ID += 1

    def test_change_courier_with_order(self):

        global COURIER_ID
        global ORDER_ID

        courier = {
            "data": [
                {
                    "courier_id": COURIER_ID,
                    "courier_type": "bike",
                    "regions": [10, 11, 12],
                    "working_hours": [
                        "09:00-18:00"
                    ]
                }
            ]
        }

        order = {
            "data": [
                {
                    "order_id": ORDER_ID,
                    "weight": 10,
                    "region": 10,
                    "delivery_hours": [
                        "12:00-14:00",
                        "18:00-00:00"
                    ]
                },
                {
                    "order_id": ORDER_ID + 1,
                    "weight": 5,
                    "region": 11,
                    "delivery_hours": [
                        "12:00-14:00",
                        "18:00-00:00"
                    ]
                },
                {
                    "order_id": ORDER_ID + 2,
                    "weight": 10,
                    "region": 12,
                    "delivery_hours": [
                        "12:30-14:00",
                        "18:00-00:00"
                    ]
                }
            ]
        }

        patch = {
            "courier_type": "foot",
            "regions": [12, 13],
            "working_hours": ["09:00-10:00", "11:00-12:00"]
        }

        assign = {
           "courier_id": COURIER_ID
        }

        res_cour = requests.post(f'http://{HOST}:{PORT}/couriers', json=courier)
        res_order = requests.post(f'http://{HOST}:{PORT}/orders', json=order)
        res_assign = requests.post(f'http://{HOST}:{PORT}/orders/assign', json=assign)
        res_patch = requests.patch(f'http://{HOST}:{PORT}/couriers/{COURIER_ID}', json=patch)

        assert res_patch.json()['courier_type'] == 'foot'
        assert res_patch.json()['regions'] == [12, 13]
        assert res_patch.json()['working_hours'] == ["09:00-10:00", "11:00-12:00"]

        order = {
            "data": [
                {
                    "order_id": ORDER_ID + 3,
                    "weight": 10,
                    "region": 13,
                    "delivery_hours": [
                        "09:00-14:00"
                    ]
                }
            ]
        }
        res_order = requests.post(f'http://{HOST}:{PORT}/orders', json=order)
        res_assign = requests.post(f'http://{HOST}:{PORT}/orders/assign', json=assign)
        assert res_assign.status_code == 200
        assert res_assign.json()['orders'][0]['id'] == ORDER_ID + 3
        couriers.append(COURIER_ID)
        orders.append(ORDER_ID)
        orders.append(ORDER_ID + 1)
        orders.append(ORDER_ID + 2)
        orders.append(ORDER_ID + 3)

    def test_clean_up(self):
        for c in couriers:
            requests.delete(f'http://{HOST}:{PORT}/couriers/delete/{c}')

        for o in orders:
            requests.delete(f'http://{HOST}:{PORT}/orders/delete/{o}')
