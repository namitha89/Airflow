from logging import exception
import requests
import os
import logging
import time
log = logging.getLogger("test")

console = logging.StreamHandler()
filehand = logging.FileHandler('crawl_url/logging_test.log')
format_str = '%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'
console.setFormatter(logging.Formatter(format_str))
filehand.setFormatter(logging.Formatter(format_str))
log.addHandler(console) 
log.addHandler(filehand)
log.setLevel(logging.DEBUG)

def get_suffix_url_list(file):
    data = []
    try :
        with (open(file, 'r')) as urls:
            results = urls.readlines()
            for res in results:
                url = str(res)
                url = url.split()
                if url and url != "":
                    data.append(url[1])
        return data
    except exception as E:
        logging.error(f"The error occured is {E}")

def get_complete_url(results, url):
    complete_urls = []
    try:
        for val in results:
            val= val.strip('"')
            link = f"{url}{val}"
            complete_urls.append(link)
        return complete_urls
    except Exception as E:
        logging.error(f"the error is {E}")

def fetch_data_from_url(list_of_urs):
    for link in list_of_urls:
        content = requests.get(link).content
        content = content.decode('ascii')
        fname = link.split("/")[-2:]
        file_name = "_".join(fname)
        file_name = file_name + ".txt"
        file = os.path.join("crawl_url/", file_name)
        with (open(file, 'w')) as fi:
            fi.writelines(content)

if __name__=='__main__':
    results = get_suffix_url_list("su_urls.txt")
    url = "https://deelay.me/5000/http://worldtimeapi.org/api/timezone/"
    list_of_urls = get_complete_url(results, url)
    t1 = time.time()
    print(t1)
    response = fetch_data_from_url(list_of_urls)
    t2 = time.time()
    print(t2)
    print(f'MultiThreaded Code Took:{t2 - t1} seconds')
