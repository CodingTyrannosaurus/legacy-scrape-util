#!/usr/bin/env python3
from importlib import import_module
import src.core.parameters as params
import src.core.errlog as errlog


# Primary entry point for runtime.
# The one constant point in a world
# that is rife with uncertainty.
def run(project):
    config,nonce = params.get_parameters(project)
    data,nonce = acquire_data(project,config,nonce)
    data = reshape_data(project,config,data)
    export_data(project,config,data)
    params.update_nonce(project,nonce)

# Acquire the data via specifid method.
# Returns data and a new set of nonce values.
def acquire_data(project,config,nonce):
    dconf = config['acquire']
    scraper = get_util('acquire',dconf['type'])
    data,nonce = scraper.scrape(project,dconf,nonce)
    return data,nonce

# Reshape the data via specified mapping(s).
def reshape_data(project,config,data):
    if not data: return
    if 'reshape' in config:
        rconf = config['reshape']
    else: return data
    rutils = {}
    rord = []
    for kind in rconf:
        if 'file' in kind: continue
        rutils[kind] = get_util('reshape',kind)
        rord.append(kind)
    skey = lambda k: rutils[k].ORD
    rord = sorted(rord,key=skey)
    for rs in rord:
        data = rutils[rs].reshape(project,rconf[rs],data)
    return data

# Save the data via specified channel(s).
def export_data(project,config,data):
    if not data:
        print('no values to export.')
        return
    exconf = config['export']
    for kind in exconf:
        exutil = get_util('export',kind)
        exutil.export(data,project,exconf[kind])

# Generic 'utility' getter.
# Attempts to take a category & kind,
# and return a library object.
def get_util(category,kind):
    modname = 'src.{}.{}'.format(category,kind).lower()
    try: mod = import_module(modname)
    except: raise Exception('no utility at: {}'.format(modname))
    return mod
