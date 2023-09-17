import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
from scipy import stats
import math
import random
from collections import Counter
import itertools
import re
import googlesearch
# %matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns

from bs4 import BeautifulSoup
import urllib
import ipaddress
import socket
import requests
import whois
from datetime import date, datetime
import time
from dateutil.parser import parse as date_parse
from urllib.parse import urlparse

#FUCNTIONS
# def having_ip_address(url):
#     match = re.search(
#         '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
#         '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
#         '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
#         '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
#     if match:
#         return 1
#     else:
#         # print 'No matching pattern found'
#         return 

def UsingIp(url):
        try:
            ipaddress.ip_address(url)
            return -1
        except:
            return 1
        


def shortUrl(url):
        shortening_services = [
    "bit.ly", "goo.gl", "shorte.st", "go2l.ink", "x.co", "ow.ly", "t.co", "tinyurl", "tr.im", "is.gd", "cli.gs",
    "yfrog.com", "migre.me", "ff.im", "tiny.cc", "url4.eu", "twit.ac", "su.pr", "twurl.nl", "snipurl.com",
    "short.to", "BudURL.com", "ping.fm", "post.ly", "Just.as", "bkite.com", "snipr.com", "fic.kr", "loopt.us",
    "doiop.com", "short.ie", "kl.am", "wp.me", "rubyurl.com", "om.ly", "to.ly", "bit.do", "lnkd.in", "db.tt",
    "qr.ae", "adf.ly", "ity.im", "q.gs", "po.st", "bc.vc", "twitthis.com", "u.to", "j.mp", "buzurl.com", "cutt.us",
    "u.bb", "yourls.org", "x.co", "prettylinkpro.com", "scrnch.me", "filoops.info", "vzturl.com", "qr.net",
    "1url.com", "tweez.me", "v.gd", "tr.im", "link.zip.net"]

        if any(service in url for service in shortening_services):
            return -1
        else:
            return 1
        
def symbol(url):
        if re.findall("@",url):
            return -1
        return 1
    
    
def redirecting(url):
    if url.rfind('//')>6:
        return -1
    return 1

def SubDomains(url):
        dot_count = len(re.findall("\.", url))
        if dot_count == 1:
            return 1
        elif dot_count == 2:
            return 0
        return -1

def DomainRegLen(url):
    domain = urlparse(url).netloc
    whois_response = whois.whois(domain)
    try:
        
        expiration_date = whois_response.expiration_date
        creation_date = whois_response.creation_date
        try:
            if(len(expiration_date)):
                expiration_date = expiration_date[0]
        except:
            pass
        try:
            if(len(creation_date)):
                creation_date = creation_date[0]
        except:
            pass
        age = (expiration_date.year-creation_date.year)*12+ (expiration_date.month-creation_date.month)
        if age >=12:
            return 1
        return -1
    except:
            return -1
        
def RequestURL(url):
    domain = urlparse(url).netloc
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        for img in soup.find_all('img', src=True):
            dots = [x.start(0) for x in re.finditer('\.', img['src'])]
            if url in img['src'] or domain in img['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for audio in soup.find_all('audio', src=True):
            dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
            if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
                success = success + 1
            i = i+1
        for embed in soup.find_all('embed', src=True):
            dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
            if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for iframe in soup.find_all('iframe', src=True):
            dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
            if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        try:
            percentage = success/float(i) * 100
            if percentage < 22.0:
                return 1
            elif((percentage >= 22.0) and (percentage < 61.0)):
                return 0
            else:
                return -1
        except:
            return 0
    except:
        return -1
        
def AnchorURL(url):
    domain = urlparse(url).netloc
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
            i,unsafe = 0,0
            for a in soup.find_all('a', href=True):
                if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                    unsafe = unsafe + 1
                i = i + 1

            try:
                percentage = unsafe / float(i) * 100
                if percentage < 31.0:
                    return 1
                elif ((percentage >= 31.0) and (percentage < 67.0)):
                    return 0
                else:
                    return -1
            except:
                return -1

    except:
            return -1

        
def LinksInScriptTags(url):
    domain = urlparse(url).netloc
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        i,success = 0,0
        
        for link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer('\.', link['href'])]
            if url in link['href'] or domain in link['href'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for script in soup.find_all('script', src=True):
            dots = [x.start(0) for x in re.finditer('\.', script['src'])]
            if url in script['src'] or domain in script['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        try:
            percentage = success / float(i) * 100
            if percentage < 17.0:
                return 1
            elif((percentage >= 17.0) and (percentage < 81.0)):
                return 0
            else:
                return -1
        except:
            return 0
    except:
        return -1
        
def ServerFormHandler(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
            if len(soup.find_all('form', action=True))==0:
                return 1
            else :
                for form in soup.find_all('form', action=True):
                    if form['action'] == "" or form['action'] == "about:blank":
                        return -1
                    elif url not in form['action'] and domain not in form['action']:
                        return 0
                    else:
                        return 1
    except:
            return -1
        
def InfoEmail(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
            if re.findall(r"[mail\(\)|mailto:?]", self.soup):
                return -1
            else:
                return 1
    except:
            return -1

    
def AbnormalURL(url):
    response = requests.get(url)
    domain = urlparse(url).netloc
    whois_response = whois.whois(domain)
    try:
            if response.text == whois_response:
                return 1
            else:
                return -1
    except:
            return -1

        
def WebsiteForwarding(url):
    response = requests.get(url)
    try:
            if len(response.history) <= 1:
                return 1
            elif len(response.history) <= 4:
                return 0
            else:
                return -1
    except:
             return -1


def StatusBarCust(url):
    response = requests.get(url)
    try:
            if re.findall("<script>.+onmouseover.+</script>", response.text):
                return 1
            else:
                return -1
    except:
             return -1

def DisableRightClick(url):
    response = requests.get(url)
    try:
            if re.findall(r"event.button ?== ?2", response.text):
                return 1
            else:
                return -1
    except:
             return -1


def UsingPopupWindow(url):
    response = requests.get(url)
    try:
            if re.findall(r"alert\(", response.text):
                return 1
            else:
                return -1
    except:
             return -1


def IframeRedirection(url):
    response = requests.get(url)
    try:
            if re.findall(r"[<iframe>|<frameBorder>]", response.text):
                return 1
            else:
                return -1
    except:
             return -1


def AgeofDomain(url):
    domain = urlparse(url).netloc
    whois_response = whois.whois(domain)
    try:
            creation_date = whois_response.creation_date
            try:
                if(len(creation_date)):
                    creation_date = creation_date[0]
            except:
                pass

            today  = date.today()
            age = (today.year-creation_date.year)*12+(today.month-creation_date.month)
            if age >=6:
                return 1
            return -1
    except:
            return -1
        
def DNSRecording(url):
    domain = urlparse(url).netloc
    whois_response = whois.whois(domain)
    try:
            creation_date = whois_response.creation_date
            try:
                if(len(creation_date)):
                    creation_date = creation_date[0]
            except:
                pass

            today  = date.today()
            age = (today.year-creation_date.year)*12+(today.month-creation_date.month)
            if age >=6:
                return 1
            return -1
    except:
            return -1
        

def WebsiteTraffic(url):
        try:
            rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
            if (int(rank) < 100000):
                return 1
            return 0
        except :
            return -1
        
def PageRank(url):
    domain = urlparse(url).netloc
    try:
            prank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {"name": domain})

            global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
            if global_rank > 0 and global_rank < 100000:
                return 1
            return -1
    except:
            return -1
            

def GoogleIndex(url):
    
        try:
            site = search(url, 5)
            if site:
                return 1
            else:
                return -1
        except:
            return 1

def prefixSuffix(url):
    domain = urlparse(url).netloc
    try:
            match = re.findall('\-', domain)
            if match:
                return -1
            return 1
    except:
            return -1

def LinksPointingToPage(url):
        response = requests.get(url)
        try:
            number_of_links = len(re.findall(r"<a href=", response.text))
            if number_of_links == 0:
                return 1
            elif number_of_links <= 2:
                return 0
            else:
                return -1
        except:
            return -1
        
def StatsReport(url):
        domain = urlparse(url).netloc
        try:
            url_match = re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly', url)
            ip_address = socket.gethostbyname(domain)
            ip_match = re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                                '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                                '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                                '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                                '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                                '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42', ip_address)
            if url_match:
                return -1
            elif ip_match:
                return -1
            return 1
        except:
            return 1



columns =[ 'UsingIP', 'LongURL', 'ShortURL', 'Symbol@', 'Redirecting//',
'PrefixSuffix-', 'SubDomains', 'HTTPS', 'DomainRegLen', 'Favicon',
'NonStdPort', 'HTTPSDomainURL', 'RequestURL', 'AnchorURL',
'LinksInScriptTags', 'ServerFormHandler', 'InfoEmail', 'AbnormalURL',
'WebsiteForwarding', 'StatusBarCust', 'DisableRightClick',
'UsingPopupWindow', 'IframeRedirection', 'AgeofDomain',
'DNSRecording', 'WebsiteTraffic', 'PageRank', 'GoogleIndex',
'LinksPointingToPage', 'StatsReport', 'class' ]

df = pd.DataFrame(columns=columns)



urls = ["https://www.google.com/"]



for url in urls:
    
    parameters = {
    'UsingIP': UsingIp(url),
    'LongURL': 1 if len(url) < 54 else (0 if 54 <= len(url) <= 75 else -1),
    'ShortURL': shortUrl(url) ,
    'Symbol@': symbol(url),
    'Redirecting//': redirecting(url),
    'PrefixSuffix-': prefixSuffix(url),
    'SubDomains': SubDomains(url),
    'HTTPS': 1 if "https://" in url else -1,
    'DomainRegLen': DomainRegLen(url),
    'Favicon': 0,
    'NonStdPort': 1 if urlparse(url).port not in (80, 443) else -1,
    'HTTPSDomainURL': 1 if "https://" in urlparse(url).netloc else -1,
    'RequestURL': RequestURL(url),
    'AnchorURL': AnchorURL(url),
    'LinksInScriptTags': LinksInScriptTags(url),
    'ServerFormHandler': ServerFormHandler(url),
    'InfoEmail': InfoEmail(url),
    'AbnormalURL': AbnormalURL(url),
    'WebsiteForwarding': WebsiteForwarding(url),
    'StatusBarCust': StatusBarCust(url),
    'DisableRightClick': DisableRightClick(url),
    'UsingPopupWindow': UsingPopupWindow(url),
    'IframeRedirection': IframeRedirection(url),
    'AgeofDomain': AgeofDomain(url),
    'DNSRecording': DNSRecording(url),
    'WebsiteTraffic': WebsiteTraffic(url),
    'PageRank': PageRank(url),
    'GoogleIndex': GoogleIndex(url),
    'LinksPointingToPage': LinksPointingToPage(url),
    'StatsReport': StatsReport(url),
    'class': 0}


    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        favicon_link = soup.find('link', rel='icon')
        if favicon_link:
            parameters['Favicon'] = 1
    except:
        pass



    df = df.append(parameters, ignore_index=True)

# Display the DataFrame
print(df)
# ChatGPT