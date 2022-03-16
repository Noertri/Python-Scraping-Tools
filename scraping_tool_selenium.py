import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from extras.loggers import INFO, create_stream_logger
from extras.terminal_bars import progress_bar


class DynamicWebScraper:
    logger = create_stream_logger(__name__, fmt="[%(levelname)s] [%(asctime)s]: %(message)s", level=INFO)
    fparser = None
    fparser_args = None
    fparser_kwargs = None
    driver = None

    def __init__(self, base_url, time_wait=-1, freq=-1):
        self.actions = None
        self.options = Options()
        self.base_url = base_url
        self.time_wait = time_wait
        self.freq = freq
        self.page_items = list()
        self.page_urls = list()

    def launch_driver(self, **kwargs):
        try:
            self.logger.info("Meluncurkan browser Chrome")
            self.driver = webdriver.Chrome(**kwargs)
            self.driver.maximize_window()
            self.actions = ActionChains(self.driver)
        except Exception:
            self.logger.info("Terjadi galat: ", exc_info=True)

    def set_new_url(self, new_url):
        self.base_url = new_url

    def _wait_all_elements_loaded_(self):
        start_time = 0
        finish_time = 0
        period = 0
        num_scroll = 0
        if float(self.time_wait) >= 5. and int(self.freq) <= 0:
            start_time = time.time()
            finish_time = start_time+float(self.time_wait)
            progress_bar(time.time(), start_time, self.time_wait)
            period = 5
        elif float(self.time_wait) >= 5. and int(self.freq) > 1:
            start_time = time.time()
            finish_time = start_time+float(self.time_wait)
            progress_bar(time.time(), start_time, self.time_wait)
            period = (self.time_wait/self.freq)

        while True:
            self.actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(period)
            progress_bar(time.time(), start_time, self.time_wait)
            if time.time() >= finish_time:
                break
            elif num_scroll >= 1000:
                break
            elif float(self.time_wait) < 0 and int(self.freq) < 0:
                break
            num_scroll += 1

    def add_parser(self, fparser, *args, **kwargs):
        self.fparser = fparser
        self.fparser_args = args
        self.fparser_kwargs = kwargs

    def add_page_urls(self, page_urls):
        self.page_urls = page_urls

    def scrape_one_page(self):
        try:
            self.driver.get(self.base_url)
            self.logger.info("Memproses halaman: {0}".format(self.driver.current_url))
        except Exception:
            self.logger.info("Terjadi galat: ", exc_info=True)
        time.sleep(5)
        self.logger.info("Menunggu semua elemen selesai dimuat")
        if self.time_wait > 0:
            self._wait_all_elements_loaded_()
        self.logger.info("Memulai scraping")
        items = self.fparser(self.driver.page_source, *self.fparser_args, **self.fparser_kwargs)
        time.sleep(3)
        self.logger.info("Hasil: {0}".format(len(items)))
        for item in items:
            self.page_items.append(item)
        time.sleep(3)
        self.logger.info("Selesai memproses")

    def scrape_all_pages(self):
        n = 0
        tic = time.time()
        for page_url in self.page_urls:
            try:
                self.base_url = page_url
                self.driver.get(self.base_url)
                self.logger.info("Memproses halaman: {0}".format(self.driver.current_url))
            except Exception:
                self.logger.info("Terjadi galat: ", exc_info=True)
            time.sleep(5)
            self.logger.info("Menunggu semua elemen dimuat")
            if self.time_wait > 0:
                self._wait_all_elements_loaded_()
            self.logger.info("Memulai scraping")
            items = self.fparser(self.driver.page_source, *self.fparser_args, **self.fparser_kwargs)
            time.sleep(3)
            self.logger.info("Hasil scraping: {0}".format(len(items)))
            for item in items:
                self.page_items.append(item)
            time.sleep(3)
            self.logger.info("Selesai memproses\n")
            n += 1
            time.sleep(3)
        toc = time.time()
        msg0 = ""
        msg1 = f"Total waktu: {(toc-tic):.2f} detik"
        msg2 = f"Total halaman: {n}"
        msg3 = "Total hasil scraping: {}".format(len(self.page_items))
        msg = "\n{}".format(" "*10).join([msg0, msg1, msg2, msg3])
        self.logger.info(msg)

    def quit(self):
        self.logger.info("Menutup webdriver")
        return self.driver.quit()

    def save_to_txt(self, file_name, **kwargs):
        self.logger.info("Menyimpan ke: {0}".format(file_name))
        with open(file_name, "w", **kwargs) as f:
            f.writelines("\n".join(self.page_items))
            self.logger.info("Tersimpan")
            f.close()

    def save_to_csv(self, file_name, field_names, **kwargs):
        self.logger.info("Menyimpan ke: {0}".format(file_name))
        with open(file_name, "w", newline="", **kwargs) as f:
            row_writer = csv.DictWriter(f, field_names, delimiter=";")
            row_writer.writeheader()
            for item in self.page_items:
                row_writer.writerow(item)
            self.logger.info("Tersimpan")
            f.close()

    def save_to_json(self, file_name, **kwargs):
        self.logger.info("Menyimpan ke: {0}".format(file_name))
        json_obj = json.dumps(self.page_items, **kwargs)
        with open(file_name, "w") as f:
            f.write(json_obj)
            self.logger.info("Tersimpan")
            f.close()