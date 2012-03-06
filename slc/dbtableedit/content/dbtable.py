"""Definition of the DBTable content type
"""
from types import *
from zope.interface import implements, directlyProvides
from zope.component import getUtility 

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from slc.dbtableedit import dbtableeditMessageFactory as _
from slc.dbtableedit.interfaces import IDBTable
from slc.dbtableedit.config import PROJECTNAME
from AccessControl import ClassSecurityInfo

from plone.memoize import instance

from schema import DBTableSchema

from collective.lead.interfaces import IDatabase
import sqlalchemy as sa



# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

DBTableSchema['title'].storage = atapi.AnnotationStorage()
DBTableSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(DBTableSchema, moveDiscussion=False)

class DBTable(base.ATCTContent):
    """Object representing a RDB Table"""
    implements(IDBTable)

    portal_type = "DBTable"
    schema = DBTableSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    security = ClassSecurityInfo()
    
    def _get_conn(self):
        conn = {}
        db = getUtility(IDatabase, name=self.getDBConnection())
        connection = db.connection 
        meta = sa.MetaData()
        meta.bind = connection
        conn['conn'] = connection
        conn['main'] = sa.Table(self.getTable(), meta, autoload=True)
        if self.getLeft_table():
            conn['left'] = sa.Table(self.getLeft_table(), meta, autoload=True)
        if self.getRight_table():
            conn['right'] = sa.Table(self.getRight_table(), meta, autoload=True)
        return conn
        
    def getColumnsOfTable(self, tablename):
        """ returns the column headers of the given table 
        """
        C = self._get_conn()
        if tablename not in ['main', 'left', 'right']:
            return 
        table = C.get(tablename, None)
        if table is None:
            return None
        return table.c
        
    @instance.memoize
    def getColWidths(self):
        """ determine practical sizes to edit the columns based on what data already is in them
        """
        results = self.selectFromTable()
        cols = self.getColumnsOfTable('main')
        lens = {}
        for line in results:
            for c in cols:
                val = line[c]
                if type(val) == UnicodeType:
                    L = len(val.encode('utf-8'))
                elif type(val) in [IntType, FloatType]:
                    L = len(str(val))
                else:
                    try: 
                        L = len(str(val))
                    except: 
                        L = 10
                        
                lens[c.name] = max(lens.get(c.name, 0), L)
                
        # find proper defaults, this could be a very evaluated statistical approach ;)
        def finddefault(num):
            if num<5: 
                return 5
            elif num>40:
                return 40
            else:
                return num
                
        for c in cols:
            lens[c.name] = finddefault(lens.get(c.name, 10))
            
        return lens                 
                                
        
    security.declareProtected('Modify portal content','selectFromTable')
    def selectFromTable(self, order=''):
        """
        Select dynamically from table
        """
        C = self._get_conn()
        conn = C['conn']
        maintable = C['main']
        sortcolumn = getattr(maintable.c, self.getSortByColumn())

        
        # check if we should filter...
        request = self.REQUEST
        WC = []
        if not request.get('form.button.RemoveFilter', None):
            for elem in request.keys():
                if elem.startswith('filter_') and request.get(elem,'') != '':
                    fieldname = elem.replace('filter_', '')
                    value = "%s%%" % request.get(elem,'')
                    WC.append(getattr(maintable.c, fieldname).like(value))

        if WC:
            cond = WC[0]
            for C in WC[1:]:
                cond = cond & C
            statement = maintable.select(cond)
            statement = statement.order_by(sortcolumn)             
            results = conn.execute(statement).fetchall() 
        else:
            statement = sa.sql.select([maintable])
            statement = statement.order_by(sortcolumn) 
            results = conn.execute(statement).fetchall() 

        return results

    security.declareProtected('Modify portal content', 'insertIntoTable')
    def insertIntoTable(self):
        """
        Inserts into table whatever is given in the request and matches the table colum names
        """
        R = self.REQUEST
        C = self._get_conn()
        conn = C['conn']
        maintable = C['main']


        toset = {}
        for c in maintable.columns:
            if R.has_key('db_%s' % c.name):
                toset[c.name] = R['db_%s'%c.name]
        
        columns = toset.keys()        
        ins = maintable.insert(toset)
        
        result = conn.execute(ins)
        id = result.last_inserted_ids()
        
        return "Record added. ID: %s" % id

    security.declareProtected('Modify portal content', 'deleteFromTable')
    def deleteFromTable(self):
        """
        deletes the selected record from the database.
        """
        C = self._get_conn()
        conn = C['conn']
        maintable = C['main']
        pkey = getattr(maintable.c, self.getPrimaryKey())

        IDS = self.REQUEST.get('IDS', '')
        if type(IDS) == type([]):
            ID = IDS[0]
                      
        delete = maintable.delete(pkey==ID)       
        result = conn.execute(delete)
        
        return "The following record has been deleted: %s." % ID


    security.declareProtected('Modify portal content','updateTable')
    def updateTable(self):
        """
        updates the given entry
        """
        R = self.REQUEST
        C = self._get_conn()
        conn = C['conn']
        maintable = C['main']
        pkey = getattr(maintable.c, self.getPrimaryKey())

        IDS = R.get('IDS', [])
        if type(IDS) == type(''):
            IDS = [IDS]
        ID = IDS[0]

        toset = {}
        for c in maintable.columns:
            if R.has_key('db_%s' % c.name):
                toset[c.name] = R['db_%s'%c.name]
        
        upd = maintable.update(pkey==ID, values=toset)
        conn.execute(upd)
        return "Record %s has been updated" % ID

    security.declareProtected('Modify portal content','getNextPKValue')
    def getNextPKValue(self):
        """ Selects the max from the primary key column and increments by one
        """
        C = self._get_conn()
        conn = C['conn']
        maintable = C['main']
        pkey = getattr(maintable.c, self.getPrimaryKey())
        statement = sa.sql.select([sa.sql.func.max(pkey).label('maxkey')])
        result = conn.execute(statement)
        maxkey = result.fetchone()['maxkey']
        if maxkey is None:
            return 0
        return maxkey+1
        
    security.declareProtected('Modify portal content','getForeignKeyList')
    @instance.memoize
    def getForeignKeyList(self, column):
        """
        retrieves a value list as specified in the property configureForeignKeys to be used in the inplace editor
        """
        data = self.getConfigureForeignKeys()
        FL = {}
        for line in data:
            elems = line.split('|')
            if len(elems)>1:
                FL[elems[0].strip()] = elems[1]
        if column not in FL.keys():
            return None
            
        C = self._get_conn()
        conn = C['conn']
        SQL = "SELECT %s" % FL[column]
        statement = sa.sql.text(SQL)
        result = conn.execute(statement)

        R = []
        for i in result:
            R.append(i[0])
        R.sort()
        return R


    def fetchNMJoin(self, lwhere='', rwhere=''):
        """ Fetches the joint information for a n-m table """
        ltab = self.getLeft_table()
        lpkey = self.getLeft_table_pkey()

        thistab = self.getTable()
        lfkey = self.getLeftForeignKey()
        rfkey = self.getRightForeignKey()

        rtab = self.getRight_table()
        rpkey = self.getRight_table_pkey()

        LCOLS = ["%s.%s AS %s_%s" %(ltab, lpkey, ltab, lpkey)]
        RCOLS = ["%s.%s AS %s_%s" %(rtab, rpkey, rtab, rpkey)]
        SQL = "SELECT "
        lcols = self.getLeft_table_display_cols().split(",")
        rcols = self.getRight_table_display_cols().split(",")
        for col in lcols:
            col = col.strip()
            LCOLS.append("%s.%s AS %s_%s" %(ltab, col, ltab, col))
        print "LCOLS:", LCOLS
        SQL += ", ".join(LCOLS)
        for col in rcols:
            col = col.strip()
            RCOLS.append("%s.%s AS %s_%s" %(rtab, col, rtab, col))
        print "RCOLS:", RCOLS
        SQL += ', ' + ", ".join(RCOLS)
        SQL += " FROM %s JOIN %s ON %s.%s=%s.%s JOIN %s ON %s.%s=%s.%s " %(ltab, thistab, ltab, lpkey, thistab, lfkey, rtab, thistab, rfkey, rtab, rpkey)
        if lwhere or rwhere:
            SQL += " WHERE "
        CONDITIONS = []
        if lwhere != '':
            CONDITIONS.append(" %s.%s=%s " %(ltab, lpkey, lwhere))
        if rwhere != '':
            CONDITIONS.append(" %s.%s=%s " %(rtab, rpkey, rwhere))
        SQL += " AND ".join(CONDITIONS)
        #print SQL
        C = getattr(self, self.getDBConnection())

        results = C().query(SQL)
        results = Results(results)
        return results

    def ajaxUpdateCell(self, id='', column='', value=None):
        """
        updates the given entry
        """
        if value is None:
            return "Error: No value given. Nothing has changed."
        if column == '':
            return "Error: Invalid Column."
        if id == '':
            return "Error: Invalid Id."
        
        C = self._get_conn()
        conn = C['conn']
        maintable = C['main']
        pkey = getattr(maintable.c, self.getPrimaryKey())

        toset = {column: value}
        upd = maintable.update(pkey==id, values=toset)
        result = conn.execute(upd)

        return value
#        
#    def getColumnData(self):
#        """
#        retrieves the data of the columns to know when to quote
#        """
#        C = getattr(self, self.getDBConnection())
#        SQL = "SELECT * FROM %s LIMIT 1;" % (self.getTable())
#        results = C().query(SQL)
#        results = Results(results)
#        names = results.names()
#        data = results.data_dictionary()
#        #print data
#        return data.copy()






    def fetchRightTableEntries(self):
        """ fetches the entries of the right table of an n-m table
        """
        return self.fetchTableEntries(self.getRight_table(),
                                      self.getRight_table_pkey(),
                                      self.getRight_table_display_cols()
                                     )

    def fetchLeftTableEntries(self):
        """ fetches the entries of the left table of an n-m table
        """
        return self.fetchTableEntries(self.getLeft_table(), self.getLeft_table_pkey(), self.getLeft_table_display_cols())


    def fetchTableEntries(self, table, pkey, cols):
        """ fetches the entries of s table of an n-m table
        """
        C = getattr(self, self.getDBConnection())
        firstrealcol = cols.split(",")
        if len(firstrealcol)>0:
            firstrealcol = firstrealcol[0].strip()
        else:
            firstrealcol = pkey
        #cols = "%s, %s" %(pkey, cols)
        SQL = "SELECT * FROM %s ORDER BY %s" % (table, firstrealcol)
        results = C().query(SQL)
        results = Results(results)
        return results, cols


    def removeListItem(self, elemid, list):
        """ removes an item from the list when dropped on the wastebin """
        elemid = elemid.replace("rec_", "")
        SQL = "DELETE FROM %s where %s=%s and %s=%s" % (self.getTable(), self.getLeftForeignKey(), list, self.getRightForeignKey(), elemid)
        C = getattr(self, self.getDBConnection())
        results = C().query(SQL)
        results = self.getRightTableEntriesByLeftId(list)
        return results




    def makeListItems(self, results, listid):
        """ Helpermethod for ajax: Takes a resultset and build a list item list from it """
        LI = ""
        tmpl = """<li id="rec_%s" class="memberrecord %s" onClick="ListItemClicked('%s', '%s', '%s')">%s</li>\n"""
        for i in range(len(results)):
            res = results[i]
            if i%2==0:
                cls = 'even'
            else:
                cls = 'odd'
            id = res[0]
            if len(res)==1:
                text = res[0]
            elif len(res)==2:
                text = res[1]
            else:
                text = ''
                for i in range(len(res)-1):
                    dat = res[i+1]
                    if dat is None:
                        dat = ''
                    else:
                        dat = str(dat)
                    text += " " + dat

            LI += tmpl %(id, cls, id, text, listid, text)

        return LI





        return self.getRightTableEntriesByLeftId(id)

    def getRightTableEntriesByLeftId(self, id):
        """
        Selects all entries from the joint table where left table id is 'id'
        """

        ltab = self.getLeft_table()
        lpkey = self.getLeft_table_pkey()

        thistab = self.getTable()
        lfkey = self.getLeftForeignKey()
        rfkey = self.getRightForeignKey()
        lsort = self.getLeft_table_sorting_col()
        rsort = self.getRight_table_sorting_col()

        rtab = self.getRight_table()
        rpkey = self.getRight_table_pkey()

        #LCOLS = ["%s.%s AS %s_%s" %(ltab, lpkey, ltab, lpkey)]
        RCOLS = ["%s.%s AS %s_%s" %(rtab, rpkey, rtab, rpkey)]
        SQL = "SELECT "
        #lcols = self.getLeft_table_display_cols().split(",")
        rcols = self.getRight_table_display_cols().split(",")
#        for col in lcols:
#            col = col.strip()
#            LCOLS.append("%s.%s AS %s_%s" %(ltab, col, ltab, col))
#        print "LCOLS:", LCOLS
#        SQL += ", ".join(LCOLS)
        for col in rcols:
            col = col.strip()
            RCOLS.append("%s.%s AS %s_%s" %(rtab, col, rtab, col))
        #print "RCOLS:", RCOLS
        SQL +=  ", ".join(RCOLS)
        SQL += " FROM %s JOIN %s ON %s.%s=%s.%s JOIN %s ON %s.%s=%s.%s " %(ltab, thistab, ltab, lpkey, thistab, lfkey, rtab, thistab, rfkey, rtab, rpkey)
        if id:
            SQL += " WHERE %s.%s=%s " %(ltab, lpkey, id)
        if rsort:
            SQL += "ORDER BY %s" % rsort
        print SQL
        C = getattr(self, self.getDBConnection())

        results = C().query(SQL)
        results = Results(results)
        results = self.makeListItems(results, id)
        return results


    def make_lefttable_clickevent(self, entry_id):
        """ generate the javascript code for the click event of a left table entry """
        jstmpl = """jQuery('#left_%s').click( function(){ fkey = %s; load_maintable();  });""" % (entry_id, entry_id)
        return jstmpl        

    def maintable(self, fkey):
        """ Load the data from the mapping (main) table """
        context = self
        C = context._get_conn()
        conn = C['conn']
        main = C['main']
        right = C['right']
        
        displaycols = [x.strip() for x in context.getRight_table_display_cols().split(',')]
        
        pkey_col = getattr(main.c, context.getPrimaryKey())
        left_fkey_col = getattr(main.c, context.getLeftForeignKey())
        right_fkey_col = getattr(main.c, context.getRightForeignKey())
        order_col = getattr(main.c, context.getRight_table_sorting_col())
        right_id_col = getattr(right.c, context.getRight_table_pkey())
        
        cols = [pkey_col]
        for name in displaycols:
            cols.append(getattr(right.c, name))
            

        from_obj = main.join(right, right_id_col==right_fkey_col)
        query = sa.sql.select(cols, from_obj=[from_obj])
        query = query.where(left_fkey_col==fkey)
        query = query.order_by(order_col)            
        
        results = conn.execute(query)
        html = []
        for line in results:
            html.append("""<li class="maintable_entry" id="main_%s">%s</li>""" % (line[right_id_col], self.display_line(line)))   
        return "\n".join(html)


    def display_line(self, line):
        """ prepares a result line for display """
        out = []
        for x in line:
            if x is None: 
                continue
            if type(x) in [IntType, FloatType]:
                x = str(x)
            elif type(x) == UnicodeType:
                x = x.encode('utf-8')

            if x.strip()=='':
                continue
            out.append(x.strip())
            
        return ", ".join(out)   


    def addEntryToList(self, id, list_id):
        """ add something to the list """
        id = int(id.split("_")[-1].strip())
        list_id = int(list_id)

        context = self
        C = context._get_conn()
        conn = C['conn']
        main = C['main']


        pkey_col = getattr(main.c, context.getPrimaryKey())
        left_fkey_col = getattr(main.c, context.getLeftForeignKey())
        right_fkey_col = getattr(main.c, context.getRightForeignKey())
        order_col = getattr(main.c, context.getRight_table_sorting_col())
        #max_pkey = conn.execute(sa.select(sa.sql.func.max(pkey_col))).fetchone()
        max_pkey = conn.execute( sa.select([sa.sql.func.max(pkey_col).label('maxid')] ) ).scalar()+1

        toset = {
                 pkey_col.name : max_pkey,
                 left_fkey_col.name: list_id,
                 right_fkey_col.name: id
                }
        ins = main.insert(values=toset)
        result = conn.execute(ins)
        id = result.last_inserted_ids()
        return self.maintable(list_id)

    def removeEntryFromList(self, id, list_id):
        """ remove something from the list """
        id = int(id.split("_")[-1].strip())
        list_id = int(list_id)

        context = self
        C = context._get_conn()
        conn = C['conn']
        main = C['main']


        pkey_col = getattr(main.c, context.getPrimaryKey())

        dele = main.delete(pkey_col==id)
        result = conn.execute(dele)
        return self.maintable(list_id)


    def update_sorting(self, list_id):
        """
        Selects all entries from the joint table where left table id is 'id'
        """
        C = self._get_conn()
        conn = C['conn']
        main = C['main']

        order = self.REQUEST.get('main[]', [])

        sortcol = getattr(main.c, self.getRight_table_sorting_col())
        fkey = getattr(main.c, self.getRightForeignKey())
        pkey = getattr(main.c, self.getPrimaryKey())

        query = main.update(pkey==sa.sql.bindparam('pkey'), values={sortcol.name: sa.sql.bindparam('counter')})
        for counter in range(len(order)):
            conn.execute(query, pkey=order[counter], counter=counter)
            
        return self.maintable(list_id)

atapi.registerType(DBTable, PROJECTNAME)
