"""
    _summary_: This spider scrapes historical quotes for a given stock symbol
    _author_:  @HarikNguyen (Khai Nguyen Le Tuan)
    _api_: https://www.stockbiz.vn/Stocks/API/HistoricalQuotes.aspx
    _api_payload_: {
        Cart_ctl00_webPartManager_wp1770166562_wp1427611561_callbackData_Callback_Param: "start at example: 2022-01-01",
        Cart_ctl00_webPartManager_wp1770166562_wp1427611561_callbackData_Callback_Param: "end at example: 2022-12-01",
        Cart_ctl00_webPartManager_wp1770166562_wp1427611561_callbackData_Callback_Param: "page at example: 1",
    }
    _api_response_: a html
    _library dependency_: scrapy, bs4
"""
# python libraries
from datetime import datetime
import json

# scrapy libraries
from scrapy import Spider, Request

# other libraries
from bs4 import BeautifulSoup


# define properties name for data
DATE = "date"  # Ngày
FLUCTUATION = "fluctuation"  # Thay đổi
OPEN = "open price"  # Mở cửa
HIGH = "high price"  # Đỉnh cao
LOW = "low price"  # Đáy thấp
CLOSE = "close price"  # Đóng cửa
AVG_PRICE = "AVG price"  # Giá trung bình
ADJUSTED_CLOSE = "adjusted close price"  # Đóng cửa điều chỉnh
VOLUME = "volume"  # Khối lượng giao dịch


class HistoricalQuotesSpider(Spider):
    name = "historical_quotes"
    start_urls = ["https://www.stockbiz.vn/Stocks/API/HistoricalQuotes.aspx"]
    custom_settings = {"ROBOTSTXT_OBEY": False}
    start_date = datetime(2009, 10, 1)
    end_date = datetime.now()
    page_number = 1
    DATE_FORMAT = "%Y-%m-%d"

    def start_requests(self):
        """
        _summary_: This function is called when the spider is opened. (activation function of the spider)
        """

        headers, payload = self.get_request_dependencies()
        print(payload)
        yield Request(
            url=self.start_urls[0],
            headers=headers,
            body=payload,
            callback=self.parse,
            dont_filter=True,
        )

    def get_request_dependencies(self, page=1):
        """
        _summary_: This function is used to get request dependencies
        _param_: page: the page number to request
        _return_: headers, payload
        """
        start = self.start_date.strftime(self.DATE_FORMAT)
        end = self.end_date.strftime(self.DATE_FORMAT)
        return (
            {
                "authority": "www.stockbiz.vn",
                "accept": "*/*",
                "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
                "accept-encoding": "gzip, deflate, br",
                "Content-Type": "application/x-www-form-urlencoded",
                "referer": "https://www.stockbiz.vn/Stocks/HistoricalQuotes.aspx",
                "origin": "https://www.stockbiz.vn",
                "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            },
            "Cart_ctl00_webPartManager_wp1770166562_wp1427611561_callbackData_Callback_Param={}&Cart_ctl00_webPartManager_wp1770166562_wp1427611561_callbackData_Callback_Param={}&Cart_ctl00_webPartManager_wp1770166562_wp1427611561_callbackData_Callback_Param={}".format(
                start, end, str(page)
            ),
        )

    def parse(self, response):
        """
        _summary_: This function is called when the response is received.
        """
        # parse response
        soup = BeautifulSoup(
            response.text.replace("<![CDATA[", "").replace("]]>", ""), "html.parser"
        )
        table = soup.find_all("table", class_="dataTable")[0]
        raw_data = table.find_all("tr")
        raw_data.pop(0)
        for row in raw_data:
            data = row.find_all("td")
            yield {
                DATE: data[0].text.replace("\r\n", "").strip(),
                FLUCTUATION: data[1].text.replace("\n", "").strip().replace(",", "."),
                OPEN: float(data[2].text.replace("\n", "").strip().replace(",", ".")),
                HIGH: float(data[3].text.replace("\n", "").strip().replace(",", ".")),
                LOW: float(data[4].text.replace("\n", "").strip().replace(",", ".")),
                CLOSE: float(data[5].text.replace("\n", "").strip().replace(",", ".")),
                AVG_PRICE: float(
                    data[6].text.replace("\n", "").strip().replace(",", ".")
                ),
                ADJUSTED_CLOSE: float(
                    data[7].text.replace("\n", "").strip().replace(",", ".")
                ),
                VOLUME: float(
                    data[8]
                    .text.replace("\n", "")
                    .strip()
                    .replace(".", "")
                    .replace(",", ".")
                ),
            }

        # if this page have data then try to get next page
        if len(raw_data) > 0:
            self.page_number += 1
            headers, payload = self.get_request_dependencies(self.page_number)
            print(payload)
            yield Request(
                self.start_urls[0],
                method="POST",
                body=payload,
                headers=headers,
                callback=self.parse,
            )
