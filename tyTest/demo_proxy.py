from bs4 import BeautifulSoup
import urllib2


of = open('proxy.txt' , 'w')

for page in range(1, 160):
    html_doc = urllib2.urlopen('http://www.xici.net.co/nn/' + str(page) ).read()
    soup = BeautifulSoup(html_doc)
    trs = soup.find('table', id='ip_list').find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        ip = tds[1].text.strip()
        port = tds[2].text.strip()
        protocol = tds[5].text.strip()
        if protocol == 'HTTP' or protocol == 'HTTPS':
            of.write('%s=%s:%s\n' % (protocol, ip, port) )
            print '%s=%s:%s' % (protocol, ip, port)

of.close()