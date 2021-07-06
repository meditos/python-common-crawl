from common_crawl.finder import product_finder_helper
from threading import Thread


class ProductFinder:

    record_list = list()

    def __init__(self, record_list, prod_function):
        self.record_list = record_list
        self.prod_function = prod_function
        # Helper
        self.stopped = False
        self.finished = False
        self.save_thread = None

    # Main handler function for the multi threading
    def start(self, savethread):
        print("[*] Starting Product Finder Thread")
        self.save_thread = savethread
        Thread(target=self.update, args=()).start()
        return self
    
    # Runs on Multi Thread
    def update(self):
        i = 0
        for record in self.record_list:
            i = i + 1
            # URL Checkers. Bad: artist-redirect, %%%,
            if len(record['url']) > 23 and record['url'].count('%') < 5 and record['url'].count('artist-redirect') < 1:
                print("[{} of {}]".format(i, len(self.record_list)))
                # Ok to download and inspect
                html_content = product_finder_helper.download_page(record)
                if html_content:
                    print("[*] Retrieved {} bytes for {}".format(len(html_content), record['url']))
                    # Collects all the pages to a list
                    product, errs = self.prod_function(html_content, record['url'])
                    if product:
                        if self.save_thread.append(product):
                            print("[Success Append]")
                        if errs:
                            print("[Errors:]")
                            for err in errs:
                                print(" *  {}".format(err))
                    else:
                        print("Failed to EXTRACT Product")
                    
            # If the thread indicator variable is set, stop the thread and resource camera resources
            if self.stopped:
                return
        self.finished = True
        
    def check_status(self):
        return self.finished

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
