"""Definition of the DBTable content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from slc.dbtableedit import dbtableeditMessageFactory as _
from slc.dbtableedit.interfaces import IDBTable
from slc.dbtableedit.config import PROJECTNAME
from AccessControl import ClassSecurityInfo

import sqlalchemy as sa

DBTableSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.TextField(
        name='description',
        widget=atapi.TextAreaWidget(
            label="Description",
            description="A description for this table. It will show up in the table view.",
            label_msgid='PloneDBTableEdit_label_description',
            description_msgid='PloneDBTableEdit_help_description',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="default"
    ),

    atapi.StringField(
        name='DBConnection',
        default='',
        widget=atapi.StringWidget
        (
            label="Database Connection",
            description="Choose a database connection to use",
            label_msgid='PloneDBTableEdit_label_DBConnection',
            description_msgid='PloneDBTableEdit_help_DBConnection',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB",
    ),

    atapi.StringField(
        name='table',
        widget=atapi.StringWidget(
            label="Tablename",
            description="The name of the table inside your database that should be used for editing and displaying.",
            label_msgid='PloneDBTableEdit_label_table',
            description_msgid='PloneDBTableEdit_help_table',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.IntegerField(
        name='default_batch_size',
        default="10",
        widget=atapi.IntegerWidget(
            label="Default batch size",
            description="The number of lines displayed by default at once. Use 0 for no batching.",
            label_msgid='PloneDBTableEdit_label_default_batch_size',
            description_msgid='PloneDBTableEdit_help_default_batch_size',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='primaryKey',
        widget=atapi.StringWidget(
            label="Primay Key",
            description="The column in the table used as primary key.",
            label_msgid='PloneDBTableEdit_label_primaryKey',
            description_msgid='PloneDBTableEdit_help_primaryKey',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.BooleanField(
        name='autoIncrementPrimaryKey',
        widget=atapi.BooleanWidget(
            label="Autoincrement Primary Key?",
            description="If your Primary Key is an integer, you can choose to have it incremented automatically when a new record is added. Note that this works only with integer keys. If you have string keys or even multiple keys, you need to enter them manually.",
            label_msgid='PloneDBTableEdit_label_autoIncrementPrimaryKey',
            description_msgid='PloneDBTableEdit_help_autoIncrementPrimaryKey',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.BooleanField(
        name='showPrimaryKey',
        default=1,
        widget=atapi.BooleanWidget(
            label="Show Primary Key field?",
            description="If selected, the primary key field will not be displayed in view or edit templates. This makes usually only sense in conjunction with Autoincrement Primary Key set to true.",
            label_msgid='PloneDBTableEdit_label_showPrimaryKey',
            description_msgid='PloneDBTableEdit_help_showPrimaryKey',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.LinesField(
        name='configureForeignKeys',
        widget=atapi.LinesWidget(
            label="Configure Foreign Keys",
            description="Format is: field | select statement to retrieve the list<br>Use this to display a selection list instead of a text input field when editing the cell. The SQL statement must return a valid list of values from another table in your database. Example: CountryCode FROM Countries.",
            label_msgid='PloneDBTableEdit_label_configureForeignKeys',
            description_msgid='PloneDBTableEdit_help_configureForeignKeys',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='sortByColumn',
        widget=atapi.StringWidget(
            label="Sorting column",
            description="Specify a column which should be used for sorting. You can specify ASC or DESC as a sorting direction after the column name.",
            label_msgid='PloneDBTableEdit_label_sortByColumn',
            description_msgid='PloneDBTableEdit_help_sortByColumn',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.BooleanField(
        name='is_nm_table',
        widget=atapi.BooleanWidget(
            label="Is this an n-m table?",
            description="If this is an n-m mapping table, you can use the assign form to populate it. To make this work you need to fill in the following configuration fields also.",
            label_msgid='PloneDBTableEdit_label_is_nm_table',
            description_msgid='PloneDBTableEdit_help_is_nm_table',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='left_table',
        widget=atapi.StringWidget(
            label="Left table name",
            description="Fill in the name of the left table that should be used to populate the n-m table",
            label_msgid='PloneDBTableEdit_label_left_table',
            description_msgid='PloneDBTableEdit_help_left_table',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='left_table_pkey',
        widget=atapi.StringWidget(
            label="Primary key of the left table",
            description="Fill in the name of the primary key column of the left table",
            label_msgid='PloneDBTableEdit_label_left_table_pkey',
            description_msgid='PloneDBTableEdit_help_left_table_pkey',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='left_table_display_cols',
        widget=atapi.StringWidget(
            label="Columns to display for the left table",
            description="Name the columns that should be used to display the records in the unser interface.",
            label_msgid='PloneDBTableEdit_label_left_table_display_cols',
            description_msgid='PloneDBTableEdit_help_left_table_display_cols',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='leftForeignKey',
        widget=atapi.StringWidget(
            label="Left Foreign Key",
            description="Name the column of this table that contains the foreign key to the left table",
            label_msgid='PloneDBTableEdit_label_leftForeignKey',
            description_msgid='PloneDBTableEdit_help_leftForeignKey',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='left_table_sorting_col',
        widget=atapi.StringWidget(
            label="Left table sorting column",
            description="If you want sortable support for this table, specify a numeric column from this table which will be used for storing the order",
            label_msgid='PloneDBTableEdit_label_left_table_sorting_col',
            description_msgid='PloneDBTableEdit_help_left_table_sorting_col',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='right_table',
        widget=atapi.StringWidget(
            label="Right table name",
            description="Fill in the name of the right table that should be used to populate the n-m table",
            label_msgid='PloneDBTableEdit_label_right_table',
            description_msgid='PloneDBTableEdit_help_right_table',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='right_table_pkey',
        widget=atapi.StringWidget(
            label="Primary key of the right table",
            description="Fill in the name of the primary key column of the right table",
            label_msgid='PloneDBTableEdit_label_right_table_pkey',
            description_msgid='PloneDBTableEdit_help_right_table_pkey',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='right_table_display_cols',
        widget=atapi.StringWidget(
            label="Columns to display for the right table",
            description="Name the columns that should be used to display the records in the unser interface.",
            label_msgid='PloneDBTableEdit_label_right_table_display_cols',
            description_msgid='PloneDBTableEdit_help_right_table_display_cols',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='rightForeignKey',
        widget=atapi.StringWidget(
            label="Right foreign key",
            description="Name the column of this table that contains the foreign key to the right table",
            label_msgid='PloneDBTableEdit_label_rightForeignKey',
            description_msgid='PloneDBTableEdit_help_rightForeignKey',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),

    atapi.StringField(
        name='right_table_sorting_col',
        widget=atapi.StringWidget(
            label="Right table sorting column",
            description="If you want sortable support for this table, specify a numeric column from this table which will be used for storing the order",
            label_msgid='PloneDBTableEdit_label_right_table_sorting_col',
            description_msgid='PloneDBTableEdit_help_right_table_sorting_col',
            i18n_domain='PloneDBTableEdit',
        ),
        schemata="config DB"
    ),


))

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
    
    
    security.declarePublic('selectFromTable')
    def selectFromTable(self, where='', order=''):
        """
        Select dynamically from table
        """
        C = getattr(self, self.getDBConnection())
        if C is None:
            return
        SQL = "SELECT * FROM %s" % (self.getTable())
        if not where:
            where = self.REQUEST.get('where', '')
        if where.strip() != "":
            # Do we have an explicit where condition?
            SQL += " WHERE %s" % where


        if order.strip() != '':
            SQL += " ORDER BY %s" % order
        elif self.getSortByColumn():
            SQL += " ORDER BY %s" % self.getSortByColumn()

        SQL +=";"
        #print SQL
        results = C().query(SQL)
        results = Results(results)
        return results

    security.declarePublic('insertIntoTable')
    def insertIntoTable(self):
        """
        Inserts into table whatever is given in the request and matches the table colum names
        """
        C = getattr(self, self.getDBConnection())
        quote = C.sql_quote__
        SQL = "SELECT * FROM %s LIMIT 1;" % (self.getTable())
        results = C().query(SQL)
        results = Results(results)
        names = results.names()
        toset = {}
        R = self.REQUEST
        for n in names:
            if R.has_key('db_'+n):
                toset[n] = R['db_'+n]

        columns = toset.keys()
        vals = []
        coldata = self.getColumnData()
        for k in columns:
            if coldata[k]['type']=='s':
                val = quote(toset[k])
            else:
                val = toset[k]
            vals.append(val)
        SQL = "INSERT INTO %s (%s) VALUES (%s)" % (self.getTable(), ", ".join(columns), ", ".join(vals))
        #print SQL
        results = C().query(SQL)
        #print results
        return "Record added."

    security.declarePublic('deleteFromTable')
    def deleteFromTable(self):
        """
        deletes the selected record from the database.
        """
        C = getattr(self, self.getDBConnection())
        quote = C.sql_quote__
        IDS = self.REQUEST.get('IDS', [])

        if type(IDS) == type(''):
            IDS = [IDS]


        coldata = self.getColumnData()
        for ID in IDS:
            if coldata[self.getPrimaryKey()]['type']=='s':
                qID = quote(ID)
            else:
                qID = ID
            SQL = "DELETE FROM %s WHERE %s=%s;" % (self.getTable(), self.getPrimaryKey(), qID)
            #print SQL
            results = C().query(SQL)
        return "The following records have been deleted: %s." % IDS

    security.declarePublic('updateTable')
    def updateTable(self):
        """
        updates the given entry
        """
        C = getattr(self, self.getDBConnection())
        quote = C.sql_quote__
        IDS = self.REQUEST.get('IDS', [])
        if type(IDS) == type(''):
            IDS = [IDS]
        ID = IDS[0]

        SQL = "SELECT * FROM %s LIMIT 1;" % (self.getTable())
        results = C().query(SQL)
        results = Results(results)
        names = results.names()
        toset = {}
        R = self.REQUEST
        coldata = self.getColumnData()

        for n in names:
            if R.has_key('db_'+n):
                toset[n] = R['db_'+n]
        vals = []
        for I in toset.items():
            if coldata[i[0]]['type']=='s':
                I[1] = quote(I[1])
            vals.append("=".join(I))
        if coldata[self.getPrimaryKey()]['type']=='s':
            qID = quote(ID)
        else:
            qID = ID
        SQL = "UPDATE %s SET %s WHERE %s=%s;" % (self.getTable(), ", ".join(vals), self.getPrimaryKey(), qID)
        #print SQL
        results = C().query(SQL)
        return "Record %s has been updated" % ID

    security.declarePublic('getNextPKValue')
    def getNextPKValue(self):
        """
        <p>Selects the max from the primary key column and increments by
        one.</p>
        """
        try:
            C = getattr(self, self.getDBConnection())
            SQL = "SELECT max(%s) FROM %s;" % (self.getPrimaryKey(), self.getTable())
            results = C().query(SQL)
            maxkey = results[1][0][0]
            if type(maxkey) == type(3):
                nextkey = maxkey +1
            else:
                nextkey = 1
            return nextkey
        except:
            return 1

    security.declarePublic('getForeignKeyList')
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
        SQL = "SELECT %s;" % FL[column]
        C = getattr(self, self.getDBConnection())
        results = C().query(SQL)
        results = Results(results)
        R = []
        for i in results:
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

    def ajaxUpdateCell(self, id, column, val):
        """
        updates the given entry
        """
        C = getattr(self, self.getDBConnection())
        quote = C.sql_quote__
        coldata = self.getColumnData()
        #print column
        if coldata[column]['type']=='s':
            qval = quote(val)
        if coldata[self.getPrimaryKey()]['type']=='s':
            qid = quote(id)
        else:
            qid = id

        SQL = "UPDATE %s SET %s=%s WHERE %s=%s;" % (self.getTable(), column, qval, self.getPrimaryKey(), qid)
        #print SQL
        results = C().query(SQL)
        return val

    def manage_insertNewLine(self, RESPONSE=None):
        """
        inserts and redirects
        """
        #print "in manage insert new line!"
        self.insertIntoTable()
        RESPONSE.redirect('edit')

    def getColumnData(self):
        """
        retrieves the data of the columns to know when to quote
        """
        C = getattr(self, self.getDBConnection())
        SQL = "SELECT * FROM %s LIMIT 1;" % (self.getTable())
        results = C().query(SQL)
        results = Results(results)
        names = results.names()
        data = results.data_dictionary()
        #print data
        return data.copy()

    def fetchRightTableEntries(self):
        """ fetches the entries of the right table of an n-m table
        """
        return self.fetchTableEntries(self.getRight_table(),
                                      self.getRight_table_pkey(),
                                      self.getRight_table_display_cols()
                                     )

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

    def fetchLeftTableEntries(self):
        """ fetches the entries of the left table of an n-m table
        """
        return self.fetchTableEntries(self.getLeft_table(), self.getLeft_table_pkey(), self.getLeft_table_display_cols())

    def removeListItem(self, elemid, list):
        """ removes an item from the list when dropped on the wastebin """
        elemid = elemid.replace("rec_", "")
        SQL = "DELETE FROM %s where %s=%s and %s=%s" % (self.getTable(), self.getLeftForeignKey(), list, self.getRightForeignKey(), elemid)
        C = getattr(self, self.getDBConnection())
        results = C().query(SQL)
        results = self.getRightTableEntriesByLeftId(list)
        return results


    def addToListItems(self, id, list):
        """ add something to the list """
        id = id.split("_")[-1]
        list = list.replace('list_', '')
        SQL = """INSERT INTO %s (%s, %s, %s) VALUES (max(%s.%s)+1, %s, %s)""" % \
                (self.getTable(),
                 self.getPrimaryKey(),
                 self.getLeftForeignKey(),
                 self.getRightForeignKey(),
                 self.getTable(),
                 self.getPrimaryKey(),
                 list,
                 id)
        #print SQL
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

    def sortRightTableEntriesByLeftId(self, id, order):
        """
        Selects all entries from the joint table where left table id is 'id'
        """
        C = getattr(self, self.getDBConnection())
        conn = C()
        print order
        print id
        thistab = self.getTable()
        sortcol = self.getRight_table_sorting_col()
        fkey = self.getRightForeignKey()
        elems = order.split("&")
        SQLS = []
        for i in range(len(elems)):
            elem = elems[i]
            k,v = elem.split('=')
            SQL = "UPDATE %s SET %s=%s WHERE %s=%s" % (thistab, sortcol, i, fkey, v)
            SQLS.append(SQL)
            #print SQL
        results = conn.query(";".join(SQLS))



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


atapi.registerType(DBTable, PROJECTNAME)
