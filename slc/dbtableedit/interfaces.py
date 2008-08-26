from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from slc.dbtableedit import dbtableeditMessageFactory as _

# -*- extra stuff goes here -*-

class IDBTable(Interface):
    """Object representing a RDB Table"""
