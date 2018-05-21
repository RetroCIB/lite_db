#!/usr/bin/env python

"""
Perform operations on sqlite3 (vendors) database.
Usage:    python lite_db.py command [arg1, ... ]
   commands:
    	create -- create new database vendors.db.
    	show   -- show contents of database.
    	add    -- add or update row to/in database.  Requires 5 args (date, trans, symbol, qty, price).
    	delete -- remove row from database.  Requires 1 arg (name).
   examples:
    python lite_db.py create
    python lite_db.py show
    python lite_db.py add 2006-01-05 BUY IBM 100.0 35.14
    python lite_db.py delete IBM
"""

import sys
import sqlite3

Values = [
    ('2006-01-05','BUY','RHAT', '100.0', '35.14'),
    ('2006-03-28','BUY','IBM', '1000.0', '45.0'),
    ('2006-04-05','BUY','MSFT', '1000.0', '72.0'),
    ('2006-04-06','SELL','IBM', '500.0', '53.0'),
    ('2018-09-08','GET','APPLE', '2000.0', '35.0'),
    ('2017-02-07','POST','ORACLE', '4000.0', '22.0'),
    ('2015-01-03','KEEP','SUN', '700.0', '13.0'),
    ]

Field_defs = [
    'date text',
    'trans text',
    'symbol text',
    'qty text',
    'price text',
    ]


def createdb():
    connection = sqlite3.connect('vendors.db')
    cursor = connection.cursor()
    q1 = "create table vendors (%s)" % (', '.join(Field_defs))
    print 'Action: %s' % q1
    cursor.execute(q1)
    q1 = "create index index1 on vendors(symbol)"
    cursor.execute(q1)
    q1 = "insert into vendors (date, trans, symbol, qty, price) values ('%s', '%s','%s', '%s',' %s')"
    for spec in Values:
        q2 = q1 % spec
        print 'Action q2: "%s"' % q2
        cursor.execute(q2)
    connection.commit()
    showdb1(cursor)
    connection.close()


def showdb():
    connection, cursor = opendb()
    showdb1(cursor)
    connection.close()


def showdb1(cursor):
    cursor.execute("select * from vendors order by symbol")
    description = cursor.description
    hr()
    rows = cursor.fetchall()
    hr()
    print 'content:'
    for row in rows:
        trans = row[1]
        date = row[0]
        symbol = '%s' % row[2]
        qty = row[3]
        price = row[4]
        print '    %s%s%s%s%s' % (
            date.ljust(12), trans.ljust(7), symbol.ljust(7), qty.ljust(7), price.ljust(7),)


def addtodb(date, trans, symbol, qty, price):
    try:
        qty = float(qty)
    except ValueError, exp:
        print 'Error: qty must be float.'
        return
    connection, cursor = opendb()
    cursor.execute("select * from vendors where symbol = '%s'" % symbol)
    rows = cursor.fetchall()
    if len(rows) > 0:
        ql = "update vendors set date='%s', trans='%s', qty='%s', price='%s' where symbol ='%s'" % (
            date, trans, qty, price, symbol)
        print 'ql:', ql
        cursor.execute(ql)
        connection.commit()
        print 'Updated'
    else:
        cursor.execute("insert into vendors values ('%s', '%s', '%s', '%s', '%s')" % (
            date, trans, symbol, qty, price))
        connection.commit()
        print 'Added'
    showdb1(cursor)
    connection.close()


def deletefromdb(name):
    connection, cursor = opendb()
    cursor.execute("select * from vendors where symbol = '%s'" % name)
    rows = cursor.fetchall()
    if len(rows) > 0:
        cursor.execute("delete from vendors where symbol='%s'" % name)
        connection.commit()
        print 'Vendor (%s) deleted.' % name
    else:
        print 'Vendor (%s) does not exist.' % name
    showdb1(cursor)
    connection.close()


def opendb():
    connection = sqlite3.connect("vendors.db")
    cursor = connection.cursor()
    return connection, cursor


def hr():
    print '-' * 60


def usage():
    print __doc__
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) < 1:
        usage()
    cmd = args[0]
    if cmd == 'create':
        if len(args) != 1:
            usage()
        createdb()
    elif cmd == 'show':
        if len(args) != 1:
            usage()
        showdb()
    elif cmd == 'add':
        if len(args) < 6:
            usage()
        date, trans, symbol, qty, price = args[1:]
#        date = args[1]
#        trans = args[2]
#        symbol = args[3]
#        qty =  args[4]
#        price = args[5]
        addtodb(date, trans, symbol, qty, price)
    elif cmd == 'delete':
        if len(args) < 2:
            usage()
        symbol = args[1]
        deletefromdb(symbol)
    else:
        usage()

if __name__ == '__main__':
    main()

