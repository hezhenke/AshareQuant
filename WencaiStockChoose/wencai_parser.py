import urllib, urllib2
from lxml import etree
import traceback

def get_wencai_stockcode(url, retry= 5, max_num= 30): 
    """
    Collects a comma-separated set of hosts (host:port) and optionally
    randomize the returned list.
    """
    while retry > 0:
        try:
            req = urllib2.Request(url=url)
            req_data = urllib2.urlopen(req, timeout=30)
            res = req_data.read()
            
            dom = etree.HTML(res.decode("utf-8",'ignore'))
            code_xpath = "//*[@id=\"tableWrap\"]/div[2]/div/div[2]//td[3]/div"
            code_divs = dom.xpath(code_xpath)
            codes = [code_div.text for code_div in code_divs]
            return codes[:max_num]
            
        except:
            traceback.print_exc()
            retry -= 1

if __name__ == "__main__":
    codes = get_wencai_stockcode("http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E5%A4%A7%E5%8D%95%E5%87%80%E9%87%8F%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%E6%8E%92%E5%88%97%3B%E5%A4%A7%E5%8D%95%E5%87%80%E9%87%8F%E5%A4%A7%E4%BA%8E0.5%3B%E6%8D%A2%E6%89%8B%E7%8E%87%E5%A4%A7%E4%BA%8E1.2%25%E5%B0%8F%E4%BA%8E5.5%25%3B%E9%87%8F%E6%AF%94%E5%B0%8F%E4%BA%8E1.8%EF%BC%9B%E6%B6%A8%E5%B9%85%E5%A4%A7%E4%BA%8E0.1%25%E5%B0%8F%E4%BA%8E7%25+")
    print str(codes)
