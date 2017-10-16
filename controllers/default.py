# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
from gluon.serializers import json
from gluon.tools import Service
import gluon.contrib.simplejson
import os
from gluon.contrib.appconfig import AppConfig

myconfig = AppConfig('app/private/appconfig.ini', reload=False)

service = Service()

"""
Default method which fetches initial data and renders the index view
"""


# function to load landing page

def index():
    return locals()


"""
Default method which fetches initial data and renders the index view
"""

# function to load data into table

def initData():
    datasource = myconfig['charts']['datasource']
    tablename = "db." + myconfig['charts']['tablename']
    tablecontrol = tablename + ".id"
    if db(eval(tablecontrol) > 0).count() == 0:
        eval(tablename).import_from_csv_file(open(datasource, 'r'))


# function to delete data in table

def truncateData():
    for entry in db.tables:
        eval('db.' + entry + '.truncate()')


#function to perform to load based chart and properties

def baseview():
    if eval(myconfig['baseview']['basechart']):
        basechartresult = db.executesql(myconfig['baseview']['basechartquery'])
        label = (myconfig['baseview']['basechartlabel1'], myconfig['baseview']['basechartlabel2'])
        basechartresult.insert(0, label)
    if eval(myconfig['baseview']['containsdropdown']):
        dropdownlist = db.executesql(myconfig['baseview']['dropdownquery'])
    if eval(myconfig['baseview']['basechart']) and eval(myconfig['baseview']['containsdropdown']):
        return dict(basechartresult=json(basechartresult), dropdownlist=json(dropdownlist), baseviewconfig=myconfig['baseview'])
    if eval(myconfig['baseview']['basechart']):
        return dict(basechartresult=json(basechartresult), baseviewconfig=myconfig['baseview'])
    if eval(myconfig['baseview']['containsdropdown']):
        return dict(dropdownlist=json(dropdownlist), baseviewconfig=myconfig['baseview'])


#function to perform ajax calls and return subchart data and properties

def subview():
    x = request.args[0]
    x = x.replace('_', ' ')
    query = myconfig['subview']['subquery'].format(x)
    subresult = db.executesql(query)
    label = (myconfig['subview']['sublabel1'], myconfig['subview']['sublabel2'])
    subresult.insert(0, label)
    result = dict()
    result['subresult'] = subresult
    result['subcharttype'] = myconfig['subview']['subcharttype']
    if eval(myconfig['subview']['subchartproperties']):
        result['haxis'] = myconfig['subview']['haxislabel']
        result['vaxis'] = myconfig['subview']['vaxislabel']
        result['vaxisformat'] = myconfig['subview']['vaxisformat']
        result['haxisformat'] = myconfig['subview']['haxisformat']
    print result
    return gluon.contrib.simplejson.dumps(result)
