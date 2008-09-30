from Acquisition import aq_inner
from types import *
from zope.interface import implements, alsoProvides
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize

from slc.dbtableedit.interfaces import IDBTableAssignView

class DBTableView(BrowserView):
    """Default view of a DBTable
    """
    
    __call__ = ViewPageTemplateFile('dbtable_view.pt')


inplace_templ = """
<script type='text/javascript'>
jq('#edit_%(id)s_%(col)s').editable({url: '%(targeturl)s', id: '%(id)s', column: '%(col)s', width: '%(width)s', typex: '%(typex)s', fkl: %(fkl)s}); 
/*jq('#edit_%(id)s_%(col)s').mouseover(function(){jq('#edit_%(id)s_%(col)s').addClass('highlighted')}).mouseout(function(){jq('#edit_%(id)s_%(col)s').removeClass( 'highlighted' )});*/
</script>
"""

class DBTableEditView(BrowserView):
    """Default edit of a DBTable
    """
    
    template = ViewPageTemplateFile('dbtable_edit.pt')
    template.id = '@@enter'

    def __call__(self):
        return self.template()
        
    
    def make_inplace_editor(self, id, col, fkl=None):
        """ generate the code for an in place editor """
        targeturl = "%s/ajaxUpdateCell" % self.context.absolute_url()
        width = self.context.getColWidths().get(col, 20)
        typex = "text"
        fklstr = '[]'
        if fkl:
            typex = "select"        
            fklstr = str(fkl)

        return inplace_templ % dict(id=id, col=col, targeturl=targeturl, width=width, typex=typex, fkl=fklstr)      
        
        
class DBTableAddRow(BrowserView):
    """ Adds a new row to the database """
    
    def __call__(self):
        """ do the insert """
        msg = self.context.insertIntoTable()
        return self.context.REQUEST.RESPONSE.redirect(self.context.absolute_url()+'/@@enter')


class DBTableDeleteRow(BrowserView):
    """ Adds a new row to the database """
    
    def __call__(self):
        """ do the delete """
        msg = self.context.deleteFromTable()
        return self.context.REQUEST.RESPONSE.redirect(self.context.absolute_url()+'/@@enter')



class DBTableAssignView(BrowserView):
    """Assign view of a DBTable
    """
    implements(IDBTableAssignView)
        
    template = ViewPageTemplateFile('dbtable_assign.pt')
    template.id = '@@assign'

    def __call__(self):
        return self.template()
        
        
    def _loadtable(self, tablename, pkey, cols, sortcol):
        """ fetches the entries of a table of an n-m table
        """
        context = aq_inner(self.context)
        C = context._get_conn()
        conn = C['conn']
        table = C[tablename]
        if cols is None:
            cols = table.c
        else:
            cols = [c for c in table.c if c.name in cols]
            
        #firstrealcol = cols.split(",")
        #if len(firstrealcol)>0:
        #    firstrealcol = firstrealcol[0].strip()
        #else:
        #    firstrealcol = pkey
        #cols = "%s, %s" %(pkey, cols)
        #SQL = "SELECT * FROM %s ORDER BY %s" % (table, firstrealcol)
        
        results = conn.execute(table.select())
        return results
        
        
    def lefttable(self):
        """ Load the data from the left table """
        context = aq_inner(self.context)
        return self._loadtable('left', 
                               context.getLeft_table_pkey(), 
                               context.getLeft_table_display_cols(),
                               context.getLeft_table_sorting_col())

        
    def righttable(self):
        """ Load the data from the right table """
        context = aq_inner(self.context)
        return self._loadtable('right', 
                               context.getRight_table_pkey(), 
                               context.getRight_table_display_cols(),
                               context.getRight_table_sorting_col())
        




                
         
        
        
