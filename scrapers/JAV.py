import base64
import datetime
import json
import re
import sys
import threading
import time

import lxml.html    # https://pypi.org/project/lxml/         | pip install lxml
import requests     # https://pypi.org/project/requests/     | pip install requests

R18_HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
    "Referer": "https://www.r18.com/"
}
JAV_HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
    "Referer": "http://www.javlibrary.com/"
}
# Print debug message
DEBUG_MODE = True
# We can't add image atm in same time as Scene
STASH_SUPPORTED = False
# Tags you don't want to see appear in Scraper window
IGNORE_TAGS = ["Features Actress","Digital Mosaic","Hi-Def","Risky Mosaic","Beautiful Girl","Blu-ray"]
# Tag you always want in Scraper window
FIXED_TAGS = "!1. JAV"

def debug(q):
    if "[DEBUG]" in q and DEBUG_MODE == False:
        return
    print(q, file=sys.stderr)

def sendRequest(url,head):
    debug("[DEBUG] Request URL: {}".format(url))
    for x in range(0,5):
        response = requests.get(url,headers=head,timeout=10)
        if response.content and response.status_code == 200:
            break
        else:
            debug("[{}] Bad page...".format(x))
            time.sleep(5)
    if response.status_code == 200:
        pass
    else:
        debug("[Request] Error, Status Code: {}".format(response.status_code))
        response=None
    return response

def regexreplace(input):
    result_regex = re.sub(r"R\*{2}e\b", "Rape", input)
    result_regex = re.sub(r"R\*{2}es\b", "Rapes", result_regex)
    result_regex = re.sub(r"R\*{4}g\b", "Raping", result_regex)
    result_regex = re.sub(r"R\*{2}ed\b", "Raped", result_regex)
    result_regex = re.sub(r"G\*{6}g\b", "Gangbang", result_regex)
    result_regex = re.sub(r"G\*{7}g\b", "Gangbang", result_regex)
    result_regex = re.sub(r"G\*{7}gs\b", "Gangbangs", result_regex)
    result_regex = re.sub(r"G\*{6}ged\b", "Gangbanged", result_regex)
    result_regex = re.sub(r"G\*{7}ged\b", "Gangbanged", result_regex)
    result_regex = re.sub(r"G\*{9}d\b", "Gang-Banged", result_regex)
    result_regex = re.sub(r"G\*{7}ging\b", "Gangbanging", result_regex)
    result_regex = re.sub(r"P\*{1}ssy\b", "Pussy", result_regex)
    result_regex = re.sub(r"C\*{1}ck\b", "Cock", result_regex)
    result_regex = re.sub(r"C\*{1}cks\b", "Cocks", result_regex)
    result_regex = re.sub(r"Ma\*{1}ko\b", "Maiko", result_regex)
    result_regex = re.sub(r"K\*{2}l\b", "Kill", result_regex)
    result_regex = re.sub(r"K\*{2}ling\b", "Killing", result_regex)
    result_regex = re.sub(r"T\*{5}e\b", "Torture", result_regex)
    result_regex = re.sub(r"T\*{5}ed\b", "Tortured", result_regex)
    result_regex = re.sub(r"V\*{5}t\b", "Violent", result_regex)
    result_regex = re.sub(r"S\*{3}e\b", "Slave", result_regex)
    result_regex = re.sub(r"S\*{3}es\b", "Slaves", result_regex)
    result_regex = re.sub(r"S\*{3}ery\b", "Slavery", result_regex)
    result_regex = re.sub(r"EnS\*{3}ed\b", "Enslaved", result_regex)
    result_regex = re.sub(r"D\*{3}king\b", "Drinking", result_regex)
    result_regex = re.sub(r"D\*{3}ks\b", "Drinks", result_regex)
    result_regex = re.sub(r"S\*{5}t\b", "Student", result_regex)
    result_regex = re.sub(r"S\*{5}ts\b", "Students", result_regex)
    result_regex = re.sub(r"SK\*{2}ls\b", "Skills", result_regex)
    result_regex = re.sub(r"SK\*{2}lfully\b", "Skillfully", result_regex)
    result_regex = re.sub(r"SK\*{2}lful\b", "Skillful", result_regex)
    result_regex = re.sub(r"SK\*{2}led\b", "Skilled", result_regex)
    result_regex = re.sub(r"P\*{4}hed\b", "Punished", result_regex)
    result_regex = re.sub(r"D\*{2}gged\b", "Drugged", result_regex)
    result_regex = re.sub(r"D\*{2}gs\b", "Drugs", result_regex)
    result_regex = re.sub(r"F\*{3}ed\b", "Fucked", result_regex)
    result_regex = re.sub(r"D\*{3}k\b", "Drunk", result_regex)
    result_regex = re.sub(r"D\*{3}kest\b", "Drunkest", result_regex)
    result_regex = re.sub(r"S\*{8}l\b", "Schoolgirl", result_regex)
    result_regex = re.sub(r"S\*{9}ls\b", "Schoolgirls", result_regex)
    result_regex = re.sub(r"S\*{8}ls\b", "Schoolgirls", result_regex)
    result_regex = re.sub(r"Sch\*{2}lgirl\b", "Schoolgirl", result_regex)
    result_regex = re.sub(r"Sch\*{2}lgirls\b", "Schoolgirls", result_regex)
    result_regex = re.sub(r"S\*{9}l\b", "School Girl", result_regex)
    result_regex = re.sub(r"P\*{4}hment\b", "Punishment", result_regex)
    result_regex = re.sub(r"P\*{4}h\b", "Punish", result_regex)
    result_regex = re.sub(r"M\*{4}ter\b", "Molester", result_regex)
    result_regex = re.sub(r"M\*{4}ters\b", "Molesters", result_regex)
    result_regex = re.sub(r"M\*{4}ted\b", "Molested", result_regex)
    result_regex = re.sub(r"M\*{4}t\b", "Molest", result_regex)
    result_regex = re.sub(r"I\*{4}t\b", "Incest", result_regex)
    result_regex = re.sub(r"I\*{4}tuous\b", "Incestuous", result_regex)
    result_regex = re.sub(r"V\*{5}e\b", "Violate", result_regex)
    result_regex = re.sub(r"V\*{5}ed\b", "Violated", result_regex)
    result_regex = re.sub(r"StepB\*{16}r\b", "StepBrother And Sister", result_regex)
    result_regex = re.sub(r"StepK\*{1}ds \b", "StepKids", result_regex)
    result_regex = re.sub(r"C\*{3}dhood\b", "Childhood", result_regex)
    result_regex = re.sub(r"V\*{6}e\b", "Violence", result_regex)
    result_regex = re.sub(r"C\*{3}dcare\b", "Childcare", result_regex)
    result_regex = re.sub(r"H\*{7}m\b", "Hypnotism", result_regex)
    result_regex = re.sub(r"M\*{4}tation\b", "Molestation", result_regex)
    result_regex = re.sub(r"M\*{4}ting\b", "Molesting", result_regex)
    result_regex = re.sub(r"F\*{3}e\b", "Force", result_regex)
    result_regex = re.sub(r"A\*{3}es\b", "Abuses", result_regex)
    result_regex = re.sub(r"A\*{3}e\b", "Abuse", result_regex)
    result_regex = re.sub(r"S\*{6}g\b", "Sleeping", result_regex)
    result_regex = re.sub(r"A\*{3}ed\b", "Abused", result_regex)
    result_regex = re.sub(r"D\*{2}g\b", "Drug", result_regex)
    result_regex = re.sub(r"A\*{5}ted\b", "Assaulted", result_regex)
    result_regex = re.sub(r"A\*{5}t", "Assault", result_regex)
    result_regex = re.sub(r"S\*{8}n\b", "Submission", result_regex)
    result_regex = re.sub(r"K\*{1}d\b", "Kid", result_regex)
    result_regex = re.sub(r"K\*{1}ds\b", "Kids", result_regex)
    result_regex = re.sub(r"D\*{6}e\b", "Disgrace", result_regex)
    result_regex = re.sub(r"Y\*{8}ls\b", "Young Girls", result_regex)
    result_regex = re.sub(r"Y\*{8}l\b", "Young Girl", result_regex)
    result_regex = re.sub(r"H\*{2}t\b", "Hurt", result_regex)
    result_regex = re.sub(r"H\*{2}ts\b", "Hurts", result_regex)
    result_regex = re.sub(r"C\*{3}dren\b", "Children", result_regex)
    result_regex = re.sub(r"F\*{3}es\b", "Forces", result_regex)
    result_regex = re.sub(r"Chai\*{1}saw\b", "Chainsaw", result_regex)
    result_regex = re.sub(r"Lol\*{1}pop\b", "Lolipop", result_regex)
    result_regex = re.sub(r"K\*{4}pped\b", "Kidnapped", result_regex)
    result_regex = re.sub(r"K\*{4}pping\b", "Kidnapping", result_regex)
    result_regex = re.sub(r"B\*{5}p\b", "Bang Up", result_regex)
    result_regex = re.sub(r"D\*{3}ken\b", "Drunken", result_regex)
    result_regex = re.sub(r"Lo\*{2}ta\b", "Lolita", result_regex)
    result_regex = re.sub(r"CrumB\*{2}d\b", "CrumBled", result_regex)
    result_regex = re.sub(r"K\*{1}dding\b", "Kidding", result_regex)
    result_regex = re.sub(r"C\*{3}d\b", "Child", result_regex)
    result_regex = re.sub(r"C\*{5}y\b", "Cruelty", result_regex)
    result_regex = re.sub(r"H\*{9}n\b", "Humiliation", result_regex)
    result_regex = re.sub(r"D\*{6}eful\b", "Disgraceful", result_regex)
    result_regex = re.sub(r"B\*{3}d\b", "Blood", result_regex)
    result_regex = re.sub(r"U\*{7}g\b", "Unwilling", result_regex)
    result_regex = re.sub(r"HumB\*{2}d\b", "Humbled", result_regex)
    result_regex = re.sub(r"K\*{2}ler\b", "Killer", result_regex)
    result_regex = re.sub(r"J\*{1}\b", "Jo", result_regex)
    result_regex = re.sub(r"J\*{1}s\b", "Jos", result_regex)
    result_regex = re.sub(r"V\*{5}es\b", "Violates", result_regex)
    result_regex = re.sub(r"D\*{6}ed\b", "Disgraced", result_regex)
    result_regex = re.sub(r"F\*{3}efully\b", "Forcefully", result_regex)
    result_regex = re.sub(r"I\*{4}ts\b", "Insults", result_regex)
    result_regex = re.sub(r"B\*{3}dy\b", "Bloody", result_regex)
    result_regex = re.sub(r"U\*{9}sly\b", "Unconsciously", result_regex)
    result_regex = re.sub(r"Half-A\*{4}p\b", "Half-Asleep", result_regex)
    result_regex = re.sub(r"A\*{4}p\b", "Asleep", result_regex)
    result_regex = re.sub(r"StepM\*{12}n\b", "Stepmother And Son", result_regex)
    result_regex = re.sub(r"C\*{3}dish\b", "Childish", result_regex)
    result_regex = re.sub(r"G\*{7}gers\b", "Gangbangers", result_regex)
    result_regex = re.sub(r"K\*{4}pper\b", "Kidnapper", result_regex)
    result_regex = re.sub(r"M\*{4}tor\b", "Molestor", result_regex)
    result_regex = re.sub(r"[\[\]\"]", "", result_regex)



    output = re.sub(r"F\*{5}g\b", "Fucking", result_regex)
    return output

def getxpath(xpath,tree):
    xPath_result=[]
    # It handle the union strangely so it better to split and do one by one
    if "|" in xpath:
        for xpath_tmp in xpath.split("|"):
            xPath_result.append(tree.xpath(xpath_tmp))
        xPath_result = [val for sublist in xPath_result for val in sublist]
    else:
        xPath_result = tree.xpath(xpath)
    #debug("xPATH: {}".format(xpath))
    #debug("raw xPATH result: {}".format(xPath_result))
    list_tmp = []
    for a in xPath_result:
        # for xpath that don't end with /text()
        if type(a) is lxml.html.HtmlElement:
            list_tmp.append(a.text_content().strip())
        else:
            list_tmp.append(a.strip())
    if list_tmp:
        xPath_result = list_tmp
    xPath_result = list(filter(None, xPath_result))
    return xPath_result

# SEARCH PAGE
def r18_search(html,xpath):
    r18_search_tree = lxml.html.fromstring(html.content)
    r18_search_url = getxpath(xpath['url'],r18_search_tree)
    r18_search_serie = getxpath(xpath['series'],r18_search_tree)
    r18_search_scene = getxpath(xpath['scene'],r18_search_tree)
    # There is only 1 scene, with serie. 
    # Could be useful is the movie already exist in Stash because you only need the name.
    if len(r18_search_scene) == 1 and len(r18_search_serie) == 1 and len(r18_search_url) == 1:
        r18_result["series_name"] = r18_search_serie
    if r18_search_url:
        r18_search_url = r18_search_url[0]
        r18_main_html = sendRequest(r18_search_url,R18_HEADERS)
        return r18_main_html
    else:
        debug("[R18] There is no result in search")
        return None

def jav_search(html,xpath):
    if "javlibrary.com/en/?v=" in html.url:
        return html
    jav_search_tree = lxml.html.fromstring(html.content)
    jav_url = getxpath(xpath['url'],jav_search_tree) # ./?v=javme5it6a
    if jav_url:
        jav_url = re.sub(r"^\.", "https://www.javlibrary.com/en", jav_url[0])
        jav_main_html = sendRequest(jav_url,JAV_HEADERS)
        return jav_main_html
    else:
        debug("[JAV] There is no result in search")
        return None

def buildlist_tagperf(data,type_scrape=""):
    list_tmp = []
    for y in data:
        if y == "":
            continue
        if type_scrape == "perf_jav":
            # Invert name
            y = re.sub(r"([a-zA-Z]+)(\s)([a-zA-Z]+)", r"\3 \1", y)
        if type_scrape == "tags" and y in IGNORE_TAGS:
            continue
        list_tmp.append({"name": y})
    # Adding personal fixed tags
    if FIXED_TAGS and type_scrape == "tags":
        list_tmp.append({"name": FIXED_TAGS})
    return list_tmp


def imagetoBase64(imageurl,typevar):
    if type(imageurl) is list:
        for image_index in range(0,len(imageurl)):
            try:
                base64image = base64.b64encode(requests.get(imageurl[image_index].replace("ps.jpg","pl.jpg"),timeout=10).content)
                imageurl[image_index] = "data:image/jpeg;base64," + base64image.decode('utf-8')
            except:
                debug("[DEBUG][{}] Failed to get the base64 of the image".format(typevar))
        if typevar == "R18Series":
            r18_result["series_image"] = imageurl
    else:
        try:
            base64image = base64.b64encode(requests.get(imageurl.replace("ps.jpg","pl.jpg"),timeout=10).content)
            if typevar == "JAV":
                jav_result["image"] = "data:image/jpeg;base64," + base64image.decode('utf-8')
            if typevar == "R18":
                r18_result["image"] = "data:image/jpeg;base64," + base64image.decode('utf-8')
            debug("[DEBUG][{}] Converted the image to base64!".format(typevar))
        except:
            debug("[DEBUG][{}] Failed to get the base64 of the image".format(typevar))
    return


fragment = json.loads(sys.stdin.read())
if fragment["url"]:
    scene_url = fragment["url"]
else:
    scene_url = None

scene_title = fragment["title"]
# Remove extension
scene_title = re.sub(r"\..{3}$", "", scene_title)
scene_title = re.sub(r"-JG\d", "", scene_title)
scene_title = re.sub(r"\s.+$", "", scene_title)
scene_title = re.sub(r"[ABCDEFGH]$", "", scene_title)

jav_search_html=None
r18_search_html=None
jav_main_html=None
r18_main_html=None

if scene_url:
    if "javlibrary.com" in scene_url:
        jav_main_html = sendRequest(scene_url,JAV_HEADERS)
    if "f50q.com" in scene_url:
        jav_main_html = sendRequest(scene_url,JAV_HEADERS)
    if "r18.com" in scene_url:
        r18_main_html = sendRequest(scene_url,R18_HEADERS)
else:
    jav_search_html = sendRequest("https://www.javlibrary.com/en/vl_searchbyid.php?keyword={}".format(scene_title),JAV_HEADERS)
    if jav_search_html is None:
        # A error for javlibrary, trying a mirror
        debug("[JAV] Error with Javlibrary, trying the mirror f50q")
        jav_search_html = sendRequest("https://www.f50q.com/en/vl_searchbyid.php?keyword={}".format(scene_title),JAV_HEADERS)
# XPATH
r18_xPath_search = {}
r18_xPath_search['series'] = '//p[text()="TOP SERIES"]/following-sibling::ul//a/span[@class="item01"]/text()'
r18_xPath_search['url'] = '//li[contains(@class,"item-list")]/a//img[string-length(@alt)=string-length(preceding::div[@class="genre01"]/span/text())]/ancestor::a/@href'
r18_xPath_search['scene'] = '//li[contains(@class,"item-list")]'

r18_xPath = {}
r18_xPath["title"] = '//section[@class="clearfix"]/div[@class="product-details"]/dl/dt[contains(.,"DVD ID")]/following-sibling::dd[1]/text()'
r18_xPath["details"] = '//div[@class="col01"]/h1/cite[@itemprop="name"]/text()|//div[contains(@class,"cmn-box-description")]/p'
r18_xPath["url"] = '//link[@rel="canonical"]/@href'
r18_xPath["date"] = '//section[@class="clearfix"]/div[@class="product-details"]/dl/dt[contains(.,"Release Date")]/../dd[@itemprop="dateCreated"]/text()'
r18_xPath["tags"] = '//div[@class="product-categories-list product-box-list"]/div[@class="pop-list"]/a'
r18_xPath["performers"] = '//div[@data-type="actress-list"]/span/a/span/text()'
r18_xPath["studio"] = '//section[@class="clearfix"]/div[@class="product-details"]/dl/dt[contains(.,"Studio")]/../dd[@itemprop="productionCompany"]/a/text()'
r18_xPath["image"] = '//meta[@itemprop="thumbnailUrl"]/@content'
r18_xPath["series_url"] = '//section[@class="clearfix"]/div[@class="product-details"]/dl/dt[contains(.,"Series:")]/following-sibling::dd[1]/a/@href'


jav_xPath_search = {}
jav_xPath_search['url'] = '//div[@class="videos"]/div/a/@title[not(contains(.,"(Blu-ray"))]/../@href'

jav_xPath = {}
jav_xPath["title"] = '//td[@class="header" and text()="ID:"]/following-sibling::td/text()'
jav_xPath["details"] = '//div[@id="video_title"]/h3/a/text()'
jav_xPath["url"] = '//meta[@property="og:url"]/@content'
jav_xPath["date"] = '//td[@class="header" and text()="Release Date:"]/following-sibling::td/text()'
jav_xPath["tags"] = '//td[@class="header" and text()="Genre(s):"]/following::td/span[@class="genre"]/a/text()'
jav_xPath["performers"] = '//td[@class="header" and text()="Cast:"]/following::td/span[@class="cast"]/span/a/text()'
jav_xPath["studio"] = '//td[@class="header" and text()="Maker:"]/following-sibling::td/span[@class="maker"]/a/text()'
jav_xPath["image"] = '//div[@id="video_jacket"]/img/@src'
jav_xPath["r18"] = '//a[text()="purchasing HERE"]/@href'

r18_result = {}
jav_result = {}

if jav_search_html:
    jav_main_html = jav_search(jav_search_html,jav_xPath_search)
    if jav_main_html is None:
        # If javlibrary don't have it, there is no way that R18 have it but why not trying...
        debug("Javlibrary don't give any result, trying search with R18...")
        r18_search_html = sendRequest("https://www.r18.com/common/search/searchword={}/?lg=en".format(scene_title),R18_HEADERS)
        r18_main_html = r18_search(jav_search_html,jav_xPath_search)


if jav_main_html:
    debug("[DEBUG] Javlibrary Page ({})".format(jav_main_html.url))
    jav_tree = lxml.html.fromstring(jav_main_html.content)
    # Get data from javlibrary
    for key,value in jav_xPath.items():
        jav_result[key] = getxpath(value,jav_tree)
    # PostProcess
    if jav_result.get("image"):
        tmp = re.sub(r"(http:|https:)", "", jav_result["image"][0])
        jav_result["image"] = "https:" + tmp
        imageBase64_jav_thread = threading.Thread(target=imagetoBase64,args=(jav_result["image"],"JAV",))
        imageBase64_jav_thread.start()
    if jav_result.get("url"):
        jav_result["url"] = "https:" + jav_result["url"][0]
    if jav_result.get("details"):
        jav_result["details"] = re.sub(r"^(.*? ){1}", "", jav_result["details"][0])
    # R18
    if jav_result.get("r18"):
        r18_search_url = re.sub(r"^redirect\.php\?url=\/\/", "https://", jav_result["r18"][0])
        r18_search_html = sendRequest(r18_search_url,R18_HEADERS)
        r18_main_html = r18_search(r18_search_html,r18_xPath_search)

# MAIN PAGE
if r18_main_html:
    debug("[DEBUG] R18 Page ({})".format(r18_main_html.url))
    r18_tree = lxml.html.fromstring(r18_main_html.content)
    # Get data from data18
    for key,value in r18_xPath.items():
        r18_result[key] = getxpath(value,r18_tree)
    # PostProcess
    # We can get the full name during the r18 search
    if r18_result.get("image"):
        r18_result["image"] = r18_result["image"][0].replace("ps.jpg","pl.jpg")
        imageBase64_r18_thread = threading.Thread(target=imagetoBase64,args=(r18_result["image"],"R18",))
        imageBase64_r18_thread.start()
    if r18_result.get("series_url"):
        r18_result['series_url'] = r18_result["series_url"][0]
        if r18_result.get("series_name") is None:
            r18_series_search = sendRequest(r18_result['series_url'],r18_tree)
            if r18_series_search is None:
                debug("[R18] Error getting to serie page")
            else:
                debug("[DEBUG] Access to series page")
                r18_series_search_tree = lxml.html.fromstring(r18_series_search.content)
                r18_result['series_name'] = r18_series_search_tree.xpath('//h1[@class="txt01"]/text()')
                xPath_series_scene = r18_series_search_tree.xpath('//li[contains(@class,"item-list")]')
                if STASH_SUPPORTED == True:
                    if len(xPath_series_scene) == 0:
                        debug("[DEBUG] Series have 0 scene")
                    else:
                        # It's useless to try to get the image there is no scene card
                        r18_result['series_image'] = r18_series_search_tree.xpath('//li[@class="item-list"]//img/@data-original')
                        imageBase64_serie_thread = threading.Thread(target=imagetoBase64,args=(r18_result["series_image"],"R18Series",))
                        imageBase64_serie_thread.start()
    else:
        if r18_result.get("series_name"):
            debug("[Warning] There is a serie but no URL ????")
        else:
            debug("[DEBUG] No series URL")
    if r18_result.get("details"):
        # Concat
        r18_result["details"] = "\n\n".join(r18_result["details"])
    if r18_result.get("date"):
        r18_date = r18_result["date"][0]
        tmp = re.sub(r"\.", "", r18_date)
        tmp = re.sub(r"Sept", "Sep", tmp)
        tmp = re.sub(r"July", "Jul", tmp)
        tmp = re.sub(r"June", "Jun", tmp)
        try:
            r18_result["date"] = str(datetime.datetime.strptime(tmp, "%b %d, %Y").date())
            pass
        except ValueError:
            r18_result["date"] = None
            pass


if r18_main_html is None and jav_main_html is None:
    debug("All request don't find anything")
    sys.exit(1)

#debug('[DEBUG][JAV] {}'.format(jav_result))
#debug('[DEBUG][R18] {}'.format(r18_result))

# Time to scrape all data
scrape = {}

# Title - Javlibrary > r18
if r18_result.get('title'):
    scrape['title'] = regexreplace(r18_result['title'][0])
if jav_result.get('title'):
    scrape['title'] = regexreplace(jav_result['title'][0])

# Date - R18 > Javlibrary
if jav_result.get('date'):
    scrape['date'] = jav_result['date'][0]
if r18_result.get('date'):
    scrape['date'] = r18_result['date']

# URL - Javlibrary > R18
if r18_result.get('url'):
    scrape['url'] = r18_result['url'][0]
if jav_result.get('url'):
    scrape['url'] = jav_result['url']

# Details - R18 > Javlibrary
if jav_result.get('details'):
    scrape['details'] = regexreplace(jav_result['details'])
if r18_result.get('details'):
    scrape['details'] = regexreplace(r18_result['details'])
if r18_result.get('series'):
    scrape['details'] = scrape['details'] + "\n\nFrom the series: " + regexreplace(r18_result['series_name'][0])

# Studio - Javlibrary > R18
scrape['studio'] = {}
if r18_result.get('studio'):
    scrape['studio']['name'] = r18_result['studio'][0]
if jav_result.get('studio'):
    scrape['studio']['name'] = jav_result['studio'][0]

# Performer - Javlibrary > R18
if r18_result.get('performers'):
    scrape['performers'] = buildlist_tagperf(r18_result['performers'])
if jav_result.get('performers'):
    scrape['performers'] = buildlist_tagperf(jav_result['performers'],"perf_jav")

# Tags - Javlibrary > R18
if r18_result.get('tags'):
    scrape['tags'] = buildlist_tagperf(r18_result['tags'],"tags")
if jav_result.get('tags'):
    scrape['tags'] = buildlist_tagperf(jav_result['tags'],"tags")

# Image - Javlibrary > R18
try:
    if imageBase64_jav_thread.is_alive() == True:
        imageBase64_jav_thread.join()
    if r18_result.get('image'):
        scrape['image'] = r18_result['image']
except NameError:
    debug("[DEBUG] No JAV Thread")
try:
    if imageBase64_r18_thread.is_alive() == True:
        imageBase64_r18_thread.join()
    if jav_result.get('image'):
        scrape['image'] = jav_result['image']
except NameError:
    debug("[DEBUG] No R18 Thread")

# Movie - R18

if r18_result.get('series_url'):
    tmp = {}
    tmp['name'] = regexreplace(r18_result['series_name'][0])
    tmp['url'] = r18_result['series_url']
    if STASH_SUPPORTED == True:
        # If Stash support this part
        if jav_result.get('image'):
            tmp['front_image'] = jav_result["image"]
        if r18_result.get('image'):
            tmp['front_image'] = r18_result["image"]
        if r18_result.get('series_image'):
            try:
                if imageBase64_serie_thread.is_alive() == True:
                    imageBase64_r18_thread.join()
                try:
                    tmp['front_image'] = r18_result["series_image"][0]
                    tmp['back_image'] = r18_result["series_image"][1]
                except:
                    pass
            except NameError:
                debug("[DEBUG] No r18 series Thread")
        if scrape.get('studio'):
            tmp['studio'] = {}
            tmp['studio']['name'] = scrape['studio']['name']
    scrape['movies'] = [tmp]

print(json.dumps(scrape))

# Last Updated May 29, 2021
