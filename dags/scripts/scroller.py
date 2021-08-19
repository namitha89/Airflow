from logging import exception
import requests
import os
import logging
import time
import datetime

log = logging.getLogger("test")
console = logging.StreamHandler()
curr_dir = os.getcwdb().decode('ascii')
log_file_path = os.path.join(curr_dir, "dags/scripts/crawl_url/logging_test.log")
filehand = logging.FileHandler(log_file_path)
format_str = '%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'
console.setFormatter(logging.Formatter(format_str))
filehand.setFormatter(logging.Formatter(format_str))
log.addHandler(console) 
log.addHandler(filehand)
log.setLevel(logging.DEBUG)

def create_directory():
    time = datetime.datetime.now()
    dt_string = time.strftime("%d_%m_%Y_%H_%M_%S")
    curr_dir = os.getcwdb().decode('ascii')
    _dir = os.path.join(curr_dir, "dags/scripts/crawl_url", f"webcrawl_{dt_string}")
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    return _dir

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

def fetch_data_from_url(list_of_urls):
    _dir = create_directory()
    for link in list_of_urls:
        content = requests.get(link).content
        content = content.decode('ascii')
        fname = link.split("/")[-2:]
        file_name = "_".join(fname)
        file_name = file_name + ".txt"
        file = os.path.join(_dir, file_name)
        with (open(file, 'w')) as fi:
            fi.writelines(content)

def get_data():
    curr_dir = os.getcwdb().decode('ascii')
    complete_file_path = os.path.join(curr_dir, "dags/scripts/su_urls.txt")
    results = get_suffix_url_list(complete_file_path)
    url = "https://deelay.me/5000/http://worldtimeapi.org/api/timezone/"
    list_of_urls = get_complete_url(results, url)
    response = fetch_data_from_url(list_of_urls)

if __name__=='__main__':
    get_data()
