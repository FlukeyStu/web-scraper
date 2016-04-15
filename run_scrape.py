#SBall 04-03-2016 - Scrape Control

#TODO: 
#   1. Fix Wayfair
#   2. Fix Go Electrical
#   3. Fix Buy It Direct
#   4. Amazon returns 0 if status "Current Unavailable"
#   5. No. Links > No. Prices??

#<span class="price"><abbr lang="en" class="currency" title="GBP">&pound;</abbr>22.49</span>
import urllib2
import csv
import sqlite3
import scrape_functions
import datetime

def db_commit(sql):
    con = sqlite3.Connection('product_scraping.db')
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
	
if __name__ == '__main__':
    con = sqlite3.Connection('product_scraping.db')
    cur = con.cursor()
    
    setup = cur.execute('SELECT run_no, feed_location FROM setup').fetchone()
    newRunNo = int(setup[0]) + 1
    feedLoc = setup[1]
    skus = []
    db_commit('UPDATE setup SET run_no='+str(newRunNo)+' ')
    with open(feedLoc, 'rb') as file:
        feed = csv.reader(file)
        for line in feed:
            if not line[0] == 'product_brand':
                skus.append(line[1])
			
    active_sites  = cur.execute('SELECT name FROM sites WHERE active = "1"').fetchall()
    
    failed = []
    for product in skus:
        #if product == '1884':
        for site in active_sites:
            print product, site[0],': ',
            select = cur.execute('SELECT url FROM links WHERE prod_code = "'+product+'" AND company = "'+site[0]+'"')
            record = select.fetchone()
            if not record == None:
                #print type(select.fetchone()[0])
                url = record[0]
                try:
                    price = scrape_functions.get_price(site[0], url)
                    print price, "\n"
                
                    cur.execute('INSERT INTO prices(run_no, product, company, price, datetime)VALUES("'+str(newRunNo)+'","'+product+'","'+site[0]+'","'+str(price)+'","'+str(datetime.datetime.now())+'")')
                except: 
                    print 'LINK FAILURE'
                    failures = (product, site[0], 'LINK FAILURE')
                    failed.append(failures)
            else:
            #except: 
                print 'NO URL'
                print '\n'
                failures = (product, site[0], 'NO URL')
                failed.append(failures)
                #continue
                #db_commit('INSERT INTO prices(run_no, product, company, price, datetime)VALUES("'+str(newRunNo)+'","'+product+'","'+site[0]+'","None","'+str(datetime.datetime.now())+'")')
        con.commit()
		
    with open('failures.txt','w') as file:
            for line in failed:
                file.write(str(line))
                file.write('\n')
                
    con.close()
