#!/usr/bin/env python3
from collections import namedtuple
import time

ORD = 4

GENERATORS = {
    'current-time' : lambda c,d: current_time(c,d)
}

def reshape(project,config,state,data):
    data = add_fields(config,data)
    return state,data

# Iterate over the configuration list,
# adding a new field for each configuration.
def add_fields(config,data):
    for field in config:
        if not field['type'] in GENERATORS:
            raise Exception('unsupported field type: '.format(field['type']))
        generate = GENERATORS[field['type']]
        if 'config' in field: field = field['config']
        data = generate(field,data)
    return data

# Adds a field containing the current time.
# Typically used to approximate an 'upload time'.
def current_time(config,data):
    name = config['name']
    fields = data[0]._fields
    newrow = namedtuple('row',[*fields,name])
    now,rows = time.time(),[]
    for row in data:
        values = list(row) + [now]
        rows.append(newrow(*values))
    return rows
