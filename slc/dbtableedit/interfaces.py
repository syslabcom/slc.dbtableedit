from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from slc.dbtableedit import dbtableeditMessageFactory as _

# -*- extra stuff goes here -*-

class IDBTable(Interface):
    """Object representing a RDB Table"""
    
class IDBTableAssignView(Interface):
    """ View for the assignment of records for an n-m table """

    def make_lefttable_clickevent(entry_id):
        """ helper to create dynamic javascript """