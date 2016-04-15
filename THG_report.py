#SB 22/3/16

import csv

con = sqlite3.Connection('product_scraping.db')
cur = con.cursor()

active_sites  = cur.execute('SELECT name FROM sites WHERE active = "1"').fetchall()

products = []





con.close()