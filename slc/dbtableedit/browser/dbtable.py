from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize

class DBTableView(BrowserView):
    """Default view of a DBTable
    """
    
    __call__ = ViewPageTemplateFile('dbtable_view.pt')


inplace_templ = """<script type="text/javascript">jq("#edit_%(id)s_%(col)s").editable({url: '%(targeturl)s', id: '%(id)s', column: '%(col)s', width: '%(width)s', typex: '%(typex)s', fkl: %(fkl)s});</script>"""

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
        width = self.context.getColWidths()[col]
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


