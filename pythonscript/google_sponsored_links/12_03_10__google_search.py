import urllib2, cookielib, re, socket, time, random, urlparse, sys

def main():           
    socket.setdefaulttimeout(60)
    outFileName = 'output.csv'
    fout = open(outFileName, 'w')
    fout.write("No. Of Ads,Ranking,Keywords,Header,Text,URL,Location,Timestamp\n")
    fout.close()
    fileName = 'file.in'
    qList = load_multi_keywords(fileName)
    count = 0
    for qs in qList:        
        count = (count + 1) % 100
        if count == 0:
            print "going to a deep sleep"
            time.sleep(random.randint(200, 400))
        try:           
            print "Query", qs             
            queryString = "+".join(qs.split())
            result = search_google(queryString)
            no_of_ads = result.__len__()
            rank = 1
            current_timestamp = int(round(time.time(), 0))            
            fout = open(outFileName, 'a')
            for item in result:
                print item
                fout.write(str(no_of_ads)+','+str(rank)+',"'+qs+'","'+item[0]+'","'+item[1]+'","'+item[2]+'","'+item[3]+'",'+str(current_timestamp)+'\n')
                rank = rank + 1
                
            fout.close()
                        
            print "\n", "going to sleep", "\n"
            time.sleep(random.randint(5, 14))
        except Exception, detail:
            print "ERROR:", detail
            continue

def load_multi_keywords(fileName):
    fp = open(fileName, 'rt')    
    keyList = fp.readlines()
    fp.close()
    qList = []
    for key in keyList:        
        if key[len(key)-1] == "\n":
            key = key[:len(key)-1]
        if key.__len__() > 3:
            qList.append(key)
    return qList


def search_google(qs):      
    url = 'http://www.google.com/search?hl=en&q='+qs+'&btnG=Google+Search'
    referer = 'http://www.google.com/'
    cj = cookielib.CookieJar()
    
    # get the first page
    try:
        print "visiting: ", url
        data, referer, cj = get_google_content(url, referer, cj)
        
        data = data.replace('<b>', '')
        data = data.replace('</b>', '')
        data = data.replace('<br>', ' ')
        
        result = parse_page(data)        
    except Exception, detail:
        print "ERROR:", detail
       
            
    return result
        
        
def get_google_content(url, referer, cj):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [
                     ('Referer', referer),
                     ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')                     
                    ]
    usock = opener.open(url)
    the_page = usock.read()
    usock.close()
    return the_page, url, cj

def parse_page(data):   
    urlPat = re.compile(r'<div id=tbd class=med>.*?>Sponsored Links</h2>(.*?)<div')
    result = re.findall(urlPat, data)    
    if result.__len__() == 0:
        print "No result found"
        return []
    data = result[0]
    
    urlPat2 = re.compile(r'<li><h3>.*?<a .*?>(.*?)</a></h3>(.*?)<cite>(.*?)</cite>([^<>]*?)<')
    result2 = re.findall(urlPat2, data)
    
    return result2
    

#program starts from here
main()
