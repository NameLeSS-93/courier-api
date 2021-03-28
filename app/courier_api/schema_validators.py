data_schema = {
    "type": "object",
    "properties":
        {
            "data": {"type": "array"}
        },
    "required": ['data']
}

courier_post_schema = {
    "type": "object",
    "properties":
        {
            "courier_id": {"type": "number"},
            "courier_type": {"type": "string"},
            "regions": {"type": "array"},
            "working_hours": {"type": "array"}
        },
    "required": ['courier_id', 'courier_type', 'regions', 'working_hours']
}

order_post_schema = {
    "type": "object",
    "properties":
        {
            "order_id": {"type": "number"},
            "weight": {"type": "number"},
            "region": {"type": "number"},
            "delivery_hours": {"type": "array"}
        },
    "required": ['order_id', 'weight', 'region', 'delivery_hours']
}

assign_post_schema = {
    "type": "object",
    "properties":
        {
            "courier_id": {"type": "number"}
        },
    "required": ['courier_id']
}

complete_post_schema = {
    "type": "object",
    "properties":
        {
            "courier_id": {"type": "number"},
            "order_id": {"type": "number"},
            "complete_time" : {"type": "string"}
        },
    "required": ['courier_id', 'order_id', 'complete_time']
}
