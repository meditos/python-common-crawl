import argparse

from common_crawl.finder.product_finder import ProductFinder
from common_crawl.save.json_save_products import JsonSaveProducts
from product.extractors import tesco_extractor
from common_crawl.utils import search_domain
import time


# Scans common crawl information for products and saves them.
def main(domain, cc_index_list, output_path):
    # Finds all relevant domins
    record_list = search_domain(domain, cc_index_list)
    # Creating save object - Products are saved to Amazon DynamoDB
    savethread = JsonSaveProducts(output_path).start()

    # Downloads page from CommconCrawl and Inspects, then Extracts infomation
    first_mid = record_list[0: int(len(record_list) / 2)]
    end_mid = record_list[int(len(record_list) / 2): int(len(record_list))]
    product_finder_1 = ProductFinder(first_mid, tesco_extractor.extract_product).start(savethread)
    product_finder_2 = ProductFinder(end_mid, tesco_extractor.extract_product).start(savethread)

    # Idle Main Thread
    while product_finder_1.check_status() is not True and product_finder_2.check_status() is not True:
        time.sleep(1)

    while savethread.alive():
        time.sleep(1)

    # Stop Threads
    product_finder_1.stop()
    product_finder_2.stop()
    savethread.stop()


if __name__ == '__main__':
    # parse the command line arguments
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-d", "--domain", required=True, help="The domain to target e.g. youtube.com")
    parser.add_argument("--index_list", nargs='+', required=True,
                        help="The index list e.g. 2017-39. Check http://index.commoncrawl.org/")
    parser.add_argument("--output_path", required=True, help="")

    args = parser.parse_args()
    main(args.domain, args.index_list, args.output_path)
