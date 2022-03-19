import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .extras import INFO, create_stream_logger, progress_bar


class DynamicWebScraper:
    _logger_ = create_stream_logger("DynamicWebScraper", fmt="[%(asctime)s] [%(levelname)s]: %(message)s", level=INFO)
    _fparser_ = None
    _fparser_args_ = tuple()
    _fparser_kwargs_ = dict()
    _driver_ = None
    _page_urls_ = list()
    _file_handler_ = None

    def __init__(self, base_url, time_wait=-1, freq=-1):
        self.base_url = base_url
        self.time_wait = time_wait
        self.freq = freq
        self.page_items = list()

    @staticmethod
    def options():
        return Options()

    def actions(self):
        try:
            return ActionChains(self._driver_)
        except Exception:
            self._logger_.info("Terjadi galat: ", exc_info=True)

    def launch(self, *args, **kwargs):
        try:
            self._logger_.info("Meluncurkan browser Chrome")
            self._driver_ = webdriver.Chrome(*args, **kwargs)
        except Exception:
            self._logger_.info("Terjadi galat: ", exc_info=True)

    @property
    def driver(self):
        try:
            return self._driver_
        except Exception:
            self._logger_.info("Terjadi galat: ", exc_info=True)

    @property
    def set_new_url(self):
        return self.base_url

    @set_new_url.setter
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
            self.actions().send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(period)
            progress_bar(time.time(), start_time, self.time_wait)
            if time.time() >= finish_time:
                break
            elif num_scroll >= 1000:
                break
            elif float(self.time_wait) < 0 and int(self.freq) < 0:
                break
            num_scroll += 1

    def add_parser_handler(self, handler, *args, **kwargs):
        self._fparser_ = handler
        self._fparser_args_ = args
        self._fparser_kwargs_ = kwargs

    @property
    def add_page_urls(self):
        return self._page_urls_

    @add_page_urls.setter
    def add_page_urls(self, page_urls):
        self._page_urls_ = page_urls

    def scrape_one_page(self):
        try:
            self._driver_.get(self.base_url)
            self._logger_.info("Memproses halaman: {0}".format(self._driver_.current_url))
        except Exception:
            self._logger_.info("Terjadi galat: ", exc_info=True)
        time.sleep(5)
        self._logger_.info("Menunggu semua elemen selesai dimuat")
        if self.time_wait > 0:
            self._wait_all_elements_loaded_()
        self._logger_.info("Memulai scraping")
        items = self._fparser_(self._driver_.page_source, *self._fparser_args_, **self._fparser_kwargs_)
        time.sleep(3)
        self._logger_.info("Hasil: {0}".format(len(items)))
        for item in items:
            self.page_items.append(item)
        time.sleep(3)
        self._logger_.info("Selesai memproses")

    def scrape_all_pages(self):
        n = 0
        tic = time.time()
        for page_url in self._page_urls_:
            try:
                self.set_new_url = page_url
                self._driver_.get(self.base_url)
                self._logger_.info("Memproses halaman: {0}".format(self._driver_.current_url))
            except Exception:
                self._logger_.info("Terjadi galat: ", exc_info=True)
            time.sleep(5)
            self._logger_.info("Menunggu semua elemen dimuat")
            if self.time_wait > 0:
                self._wait_all_elements_loaded_()
            self._logger_.info("Memulai scraping")
            items = self._fparser_(self._driver_.page_source, *self._fparser_args_, **self._fparser_kwargs_)
            time.sleep(3)
            self._logger_.info("Hasil scraping: {0}".format(len(items)))
            for item in items:
                self.page_items.append(item)
            time.sleep(3)
            self._logger_.info("Selesai memproses\n")
            n += 1
            time.sleep(3)
        toc = time.time()
        msg0 = ""
        msg1 = f"Total waktu: {(toc-tic):.2f} detik"
        msg2 = f"Total halaman: {n}"
        msg3 = "Total hasil scraping: {}".format(len(self.page_items))
        msg = "\n{}".format(" "*10).join([msg0, msg1, msg2, msg3])
        self._logger_.info(msg)

    def quit(self):
        self._logger_.info("Menutup webdriver")
        return self._driver_.quit()