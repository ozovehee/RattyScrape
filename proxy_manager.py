import requests
import internal_logger
import time

def validate_proxy(proxy, url):
    logger = internal_logger.get_logger("proxy")
    #returns boolean
    proxies = {
        "http" : proxy,
        "https" : proxy
    }
    try:
        res = requests.get(url, proxies=proxies)
    except OSError as e:
        logger.warning(f"Proxy: {proxy} returned connection error on webpage: {url}.")
        return False

    if not res.status_code == 200:
        logger.warning(f"Validation for proxy: {proxy} on webpage: {url} failed.")
        return False
    
    logger.info(f"Valid proxy: {proxy} on webpage: {url}.")
    return True

def rank_proxies(proxy_list, url):
    proxy_speeds = {}
    ranked_proxies = []
    non_valid_proxies = []
    for proxy in proxy_list:
        start_time = time.time()
        valid = validate_proxy(proxy, url)
        end_time = time.time()
        if valid:
            proxy_speeds[proxy] = end_time - start_time
        else:
            non_valid_proxies.append(proxy)

    ranked_proxies = sorted(proxy_speeds, key=proxy_speeds.get)
    return ranked_proxies



