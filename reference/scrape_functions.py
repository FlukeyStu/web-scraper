#SBall 01-03-16 - Scrape Functions

import urllib2
import mechanize

#TODO 
#	return all as floats
#	return price find failure as 888888.99 NOT IN LINE
#       differentiate between dea links (not in line) and cant get price
#       Functions with multiple defs can't differentiate between 888888 and 9999999

#DEFINITIONS
#   999999.99 == can't find price on site

def nums_only(num):
    allowed = ['0','1','2','3','4','5','6','7','8','9','.',',']
    newNum = ''
    for char in num:
        #print char, newNum
        if char in allowed:
            newNum = newNum + char
            #print newNum
    try:
        newNum = float(newNum)
        return newNum
    except: return None

def get_html(url):
    try:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.set_handle_refresh(False)
        br.addheaders=[('User-agent','Firefox')]
        response = br.open(url)
        html = response.read()
        
        return html
    except:
        return None
        
def scrape(url, tag):
    html = get_html(url)
    
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if tag in line:
                    print line
                    l = next(file).split(';')[1].strip()
                    #print l
                    try:
                        return float(nums_only(l))
                    except: return '999999.99'
            return '888888.99'
def scrape_buyit(url):
    def buyit_norm():
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'itemprop="price" ' in line:
                   # print line
                    l = line.split('"')[3]
                    try:
                        return float(nums_only(l))
                    except: return None
            return None #NOT IN LINE
                    
    def buyit_special():
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'id="wop" ' in line:
                   # print line
                    l = line.split(';')[1].split('<')[0]
                    try:
                        return float(nums_only(l))
                    except: return None
            return None #NOT IN LINE
    html = get_html(url)
    #print html
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        if not buyit_norm() == None:
            return buyit_norm()
        elif not buyit_special() == None:
            return buyit_norm()
        else: return '999999.99'
        
			 
def scrape_wayfair(url):
    html = get_html(url)
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'property="og:price:amount"' in line:
                    try:
                        return float(nums_only(line.split('=')[3].split('"')[1]))
                    except: return '999999.99'
            return '999999.99' #NOT IN LINE
    else: return None
                    
def scrape_hof(url):
    def hof_normPrice():
         with open('fullhtml.txt','rb') as rawFile:
                file = iter(rawFile)
                for line in file:
                    if 'class="price"' in line:
                        #print line
                        file.next()
                        file.next()
                        file.next()
                        try:
                            return  float(nums_only(file.next()))
                        except: return None
                return None #NOT IN LINE       
                
    def hof_specialPrice():
        with open('fullhtml.txt','rb') as rawFile:
                file = iter(rawFile)
                for line in file:
                    if 'class="priceNow "' in line:
                        #print line
                        file.next()
                        file.next()
                        file.next()
                        file.next()
                        file.next()
                        file.next()
                        try:
                            return  float(nums_only(file.next()))
                        except: return None
                return None #NOT IN LINE   
                
    html = get_html(url)
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        #normPrice = hof_normPrice()
        #specialPrice = hof_specialPrice()
        if not hof_normPrice() == None:
            return hof_normPrice()
        elif not hof_specialPrice() == None:
            return hof_specialPrice()
        else: 
			return '999999.99'
    else: return None
    
def scrape_John_Lewis(url):
    return scrape(url, 'itemprop="price"')
    
def scrape_argos(url):
    def argos_special():
        html = get_html(url)
        if not html == None:
            with open('fullhtml.txt','w') as file:
                file.write(html)
            with open('fullhtml.txt','rb') as rawFile:
                file = iter(rawFile)
                for line in file:
                    if '<span class="price"' in line:
                        l = line.split('>')[3].split('<')[0]
                        #print l
                        try:
                            return float(nums_only(l))
                        except: return None
                return None
    def multi():
        html = get_html(url)
        
        if not html == None:
            with open('fullhtml.txt','w') as file:
                file.write(html)
            with open('fullhtml.txt','rb') as rawFile:
                file = iter(rawFile)
                for line in file:
                    if '<span class="price">&pound;' in line:
                        l = line.split('>')[1].split('<')[0]
                        #print l
                        try:
                            return float(nums_only(l))
                        except: return None
                return None #NOT IN LINE
    if not scrape(url, '<li class="price" data-el="pdp-price">') == None:
        return scrape(url, '<li class="price" data-el="pdp-price">')
    elif not multi() == None:
        print 'multi',
        return multi()
    elif not argos_special() == None:
        print 'special',
        return argos_special()
    else: return '999999.99'
    
def scrape_amazon(url):
    def nextLine():
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'META NAME="ROBOTS' in line:
                    print 'ROBOTS',
                    return 'ROBOTS'
                elif '<span class="a-size-medium a-color-price">' in line:
                    l = next(file).strip()
                    print l
                    try:
                        return float(nums_only(l))
                    except: return None
                else: return None
    def sameLine():
        print 'SameLine'
        with open('fullhtml.txt','r') as rawFile:
            for line in rawFile:
                print line
                if 'class="a-size-medium a-color-price">' in line:
                    #print line
                    try:
                        return float(nums_only(line.split('>')[1].split('<')[0]))
                    except: return None
                else: return None
    html = get_html(url)
    if not html == None:
        #print html
        with open('fullhtml.txt', 'w') as file:
            file.write(html)
        if not nextLine() == None:
            return nextLine()
        elif not sameLine() == None:
            return sameLine()
        else: return '999999.99'
    else:
        return 'NO HTML'
    
def scrape_The_Hut(url):
    html = get_html(url)
    #print html
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'itemprop="price"' in line:
                    print line, 'ewds'
                    l = next(file).split(';')[1].strip()
                    try:
                        return float(nums_only(l))
                    except: return '999999.99'
    return '999999.99'
def scrape_Go_Electrical(url):
    html = get_html(url)
    
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'class="price" ' in line:
                    if not 'old-price' in line:
                        res = nums_only(next(file).split('<')[0].strip())
                        try:
                            return float(res)
                        except: return '999999.99'
       
def scrape_AO(url):
    def AOnormalPrice():
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'class="normal-price price"' in line:
                    #print line
                    try:
                        return float(nums_only(line.split(';')[1].split('<')[0].strip()))
                    except: return None
            return None
					
                    
    def AOspecialPrice():
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'class="now"' in line:
                    #print file.next()
                    try:
                        return float(nums_only(file.next().split(';')[1].split('<')[0].strip()))
                    except: return None
            return None
    html = get_html(url)
    #print html
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        #AOnormPrice = normalPrice()
        #AOspecialPrice = specialPrice()
        if not AOnormalPrice() == None:
            return AOnormalPrice()
        elif not AOspecialPrice() == None:
            return AOspecialPrice()
        else: return '999999.99'
    
def scrape_ecookshop(url):
    html = get_html(url)
    
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'itemprop="price"' in line:
                    try:
                        return float(nums_only(line.split('>')[4].split('<')[0]))
                    except: return '999999.99'
            return '888888.99'
def scrape_priceLover(url):
    html = get_html(url)
    
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'strong itemprop="price"' in line:
                    #print line
                    try:
                        return float(line.split(';')[1].split('<')[0].strip())
                    except: return '999999.99'
                return '888888.99'
def scrape_worldstores(url):
    html = get_html(url)
    
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'itemprop="price"' in line:
                    #print line
                    try:
                        return float(line.split('=')[2].split('"')[1].strip())
                    except: return '999999.99'
            return '888888.99'        
def scrape_tesco(url):
    html = get_html(url)
    
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if '<div class="price-info">' in line:
                    file.next()
                    file.next()
                    file.next()
                    file.next()
                    file.next()
                    file.next()
                    result = nums_only(file.next())
                    try:
                        return float(result)
                    except: return '999999.99'
            return '888888.99'

def scrape_dunelm(url):
    html = get_html(url)
    
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'itemprop="price"' in line:
                    res = file.next().split(';')[1].strip()
                    try:
                        return float(nums_only(res))
                    except: return '999999.99'
            return '888888.99'
                    
def scrape_robDyas(url):
    def RBnorm_Price():
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'class="regular-price"' in line:
                    if not 'related' in line:
                        try:
                            return float(nums_only(file.next().split('>')[1].split('<')[0].strip()))
                        except: return None
            return '888888.99'
            
    def RBpack_Price():
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'div class="price-info"' in line:
                    file.next()
                    file.next()
                    try:
                        return float(nums_only(file.next().split('>')[1].split('<')[0].strip()))
                    except: return None
            return '888888.99'
            
    def RBspecial_Price():
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'class="special-price"' in line:
                    file.next()
                    if not 'related' in file.next():
                        try:
                            return float(nums_only(file.next().split('<')[0].strip()))
                        except: return None
            return '888888.99'
            
    html = get_html(url)
    
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        if not RBnorm_Price() == None:
            return RBnorm_Price()
        elif not RBspecial_Price() == None:
            return RBspecial_Price()
        elif not RBpack_Price() == None:
            return RBpack_Price()
        else: return '999999.99'
                    
def scrape_brennands(url):
    html = get_html(url)
    #print html
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if '<strong>Price:</strong>' in line:
                    nxtRes = nums_only(file.next().split('>')[1].split('<')[0].strip())
                    try:
                        return float(nums_only(line.split('>')[2].strip()))
                    except:
                        try:
                            return float(nxtRes)
                        except: return '999999.99'
			return '888888.99'
			
def get_price(co, url):
	if co == 'AMAZON':
		return scrape_amazon(url)
	elif co == 'BRENNANDS':
		return scrape_brennands(url)
	elif co == 'ROBERT DYAS':
		return scrape_robDyas(url)
	elif co == 'DUNELM':
		return scrape_dunelm(url)
	elif co == 'TESCO':
		return scrape_tesco(url)
	elif co == 'WORLDSTORES':
		return scrape_worldstores(url)
	elif co == 'PRICE LOVER':
		return scrape_priceLover(url)
	elif co == 'E-COOKSHOP':
		return scrape_ecookshop(url)
	elif co == 'AO':
		return scrape_AO(url)
	elif co == 'GO ELECTRICAL':
		return scrape_Go_Electrical(url)
	elif co == 'THE HUT':
		return scrape_The_Hut(url)
	elif co == 'ARGOS':
		return scrape_argos(url)
	elif co == 'JOHN LEWIS':
		return scrape_John_Lewis(url)
	elif co == 'HOUSE OF FRASER':
		return scrape_hof(url)
	elif co == 'WAYFAIR':
		return scrape_wayfair(url)
	
def scrape_crampton(url):
    def crampton_normPrice():
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'class="price"' in line:
                    #print line
                    if not nums_only(line.split('>')[1].split('<')[0].strip()) == None:
                        return nums_only(line.split('>')[1].split('<')[0].strip())
                    else: return '999999.99'
                
    def crampton_specialPrice():
        with open('fullhtml.txt','rb') as rawFile:
            file = iter(rawFile)
            for line in file:
                if 'class="price-label">Special Price:</span>' in line:
                    file.next()
                    price = nums_only(file.next().split("<")[0].strip())
                    if not price == None:
                        return price
                    else: return '999999.99'
    html = get_html(url)
    
    if not html == None:
        with open('fullhtml.txt','w') as file:
            file.write(html)
        if not crampton_normPrice() == '':
            return 'tt'#crampton_normPrice()
        elif not crampton_specialPrice() == None:
            return crampton_specialPrice()
        else: return '999999.99'
   
	
if __name__ == '__main__':

    print 'C&M:', scrape_crampton('http://www.cramptonandmoore.co.uk/home-and-kitchen/microwaves/swan-sm22030gn-green-retro-800w-digital-freestanding-microwave.html')
    #print 'Buy It Direct: ',scrape_buyit("http://www.appliancesdirect.co.uk/p/candy%20floss%20maker/gourmet-gadgetry-candy_floss_maker-ice-cream-maker")
	#print 'John Lewis: ', scrape_John_Lewis("http://www.johnlewis.com/894kjgjvrtyiittyidyiating-60cm-wide-white/p")
    #print 'Argos: ',scrape_argos('http://www.argos.co.uk/beta/static/Product/partNumber/3325067.htm')
    #print 'Amazon: ',scrape_amazon('http://www.amazon.co.uk/gp/product/B00NFFAW50?redirect=true&ref_=s9_simh_gw_p147_d15_i3')
    #print 'E-Cookshop: ',scrape_ecookshop('http://www.ecookshop.co.uk/ecookshop/product.asp?pid=KSM156BCA')
    #print 'Wayfair: ',scrape_wayfair('http://www.wayfair.co.uk/2.7L-Pressure-Cooker-46640-MQQ1367.html')
    #print 'HOF: ',scrape_hof('http://www.houseoffraser.co.uk/null+Tilden+Suit/tildensuit_Grey,default,pd.html')
    #print 'The Hut: ',scrape_The_Hut("http://www.thehut.com/redken-pump-1000ml/10801203.html") 
    #print 'Go Electrical: ',scrape_Go_Electrical("http://www.go-electrical.co.uk/tv-radio/av-and-audio-accessories/pure-accessories-carry-case-in-real-black-leather-for-pocket-dab1500.html") 
    #print 'AO: ',scrape_AO("http://ao.com/product/172003-morphy-richards-accents-espresso-coffee-machine-black-37719-66.aspx")
    #print 'Price Lover: ',scrape_priceLover('https://www.pricelover.com/product/Dimplex_CLB20R_Club_-_Traditionally_Styled_Optiflame_Effect_Electric_Stove_-_2_Kilowatt_/CLB20R/')
    #print 'Worldstores: ', scrape_worldstores('http://www.worldstores.co.uk/p/Firstlight%20Zeta%20Pendant%20Light%20in%20Cream')
    #print 'Tesco: ',scrape_tesco('http://www.tesco.com/direct/bosch-village-jug-kettle-17l-black/455-1916.prd?pageLevel=&skuId=455-1916')
    #print 'Dunelm: ',scrape_dunelm('http://www.dunelm.com/product/delonghi-icona-kbov3001-beige-kettle-1000049138?cmCategoryId=34322')
    #print 'Robert Dyas: ', scrape_robDyas('http://www.robertdyas.co.uk/prestige-1-7l-jug-kettle-silver')
    #print 'Brennands:',scrape_brennands('http://www.brennands.co.uk/home-garden/cleaning-laundry/steam-mops/vax-steam-mop-/-cleaner-steam-fresh-combi-10-1600w-s86-sf-c/prod_5352.html')
