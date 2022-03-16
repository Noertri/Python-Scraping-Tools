import requests
import time


def scrape_one_page(base_url, scraper, **kwargs):
    r = requests.get(base_url, **kwargs)
    print("Memproses halaman: ", r.url)
    time.sleep(3)
    if r.status_code <= 200:
        print(f"Status: ", r.status_code)
        items = scraper(r.content)
        print("Hasil: ", len(items))
        print("Selesai........")
        return items
    else:
        raise ValueError(f"Status: {r.status_code}")


def scrape_all_pages(base_url, page_urls, num_pages, scraper, **kwargs):
    complete_item = list()
    for url in page_urls(base_url, num_pages):
        r = requests.get(url, **kwargs)
        print("Memproses halaman: ", r.url)
        time.sleep(3)
        if r.status_code <= 200:
            print(f"[OK]Status: ", r.status_code)
            items = scraper(r.content)
            time.sleep(3)
            print("Hasil: ", len(items))
            for item in items:
                complete_item.append(item)
            time.sleep(3)
        else:
            raise ValueError(f"Status: {r.status_code}")
        print("Selesai........")
    print(f"Hasil total: {len(complete_item)}")
    return complete_item