from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from slc.dbtableedit import dbtableeditMessageFactory as _


DBTableSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

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
        required=True,
        schemata="Database"
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
        required=True,
        schemata="Database"
    ),
    atapi.StringField(
        name='primaryKey',
        widget=atapi.StringWidget(
            label="Primary Key",
            description="The column in the table used as primary key.",
            label_msgid='PloneDBTableEdit_label_primaryKey',
            description_msgid='PloneDBTableEdit_help_primaryKey',
            i18n_domain='PloneDBTableEdit',
        ),
        required = True,
        schemata="Database"
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
        required=True,
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
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
        schemata="Database"
    ),


))
