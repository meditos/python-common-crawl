import requests
import json


# Searches the Common Crawl Index for a domain.
def search_domain(domain, index_list):
    record_list = []
    print("[*] Trying target domain: %s" % domain)

    for index in index_list:
        print("[*] Trying index %s" % index)
        cc_url = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
        cc_url += "url=%s&output=json" % domain
        response = requests.get(cc_url)
        if response.status_code == 200:
            records = response.content.splitlines()
            for record in records:
                record_list.append(json.loads(record))
            print("[*] Added %d results." % len(records))
    print("[*] Found a total of %d hits." % len(record_list))
    return record_list
