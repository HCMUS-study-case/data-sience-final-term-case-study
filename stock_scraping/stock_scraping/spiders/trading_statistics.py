"""
    _summary_: This spider is used to get trading statistics of a stock
    _author_:  @HarikNguyen (Khai Nguyen Le Tuan)
    _api_: https://www.stockbiz.vn/Stocks/API/TradingStatistics.aspx
    _api_payload_: {
        Cart_ctl00_webPartManager_wp425243205_wp378545232_cbTradingResult_Callback_Param: "start at example: 2022-01-01",
        Cart_ctl00_webPartManager_wp425243205_wp378545232_cbTradingResult_Callback_Param: "end at example: 2022-12-01",
        Cart_ctl00_webPartManager_wp425243205_wp378545232_cbTradingResult_Callback_Param: "page at example: 1",
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
CLOSE_PRICE = "close_price"  # Giá đóng cửa
TRADING_BUY_COUNT = "trading_buy_count"  # Số lượng giao dịch mua
TRADING_BUY_VOLUME = "trading_buy_volume"  # Khối lượng giao dịch mua
TRADING_SELL_COUNT = "trading_sell_count"  # Số lượng giao dịch bán
TRADING_SELL_VOLUME = "trading_sell_volume"  # Khối lượng giao dịch bán
BUY_SELL_DIFFERENCE = "buy_sell_difference"  # Chênh lệch mua bán
AUCTION_VOLUME = "auction_volume"  # Khối lượng khớp lệnh
AUCTION_VALUE = "auction_value (1000VND)"  # Giá trị khớp lệnh


class TradingStatisticsSpider(Spider):
    name = "trading_statistics"
    start_urls = ["https://www.stockbiz.vn/Stocks/API/TradingStatistics.aspx"]
    custom_settings = {"ROBOTSTXT_OBEY": False}
    start_date = datetime(2009, 10, 1)
    end_date = datetime.now()
    page_number = 1
    DATE_FORMAT = "%Y-%m-%d"
    PAYLOAD_TEMPLATE = "Cart_ctl00_webPartManager_wp425243205_wp378545232_cbTradingResult_Callback_Param={}&Cart_ctl00_webPartManager_wp425243205_wp378545232_cbTradingResult_Callback_Param={}&Cart_ctl00_webPartManager_wp425243205_wp378545232_cbTradingResult_Callback_Param={}"

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

    def get_request_dependencies(self, page_number=1):
        """
        _summary_: This function is used to get request dependencies
        _param_: page_number
        _return_: headers, payload
        """
        start_date = self.start_date.strftime(self.DATE_FORMAT)
        end_date = self.end_date.strftime(self.DATE_FORMAT)
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
            self.PAYLOAD_TEMPLATE.format(start_date, end_date, str(page_number)),
        )

    def parse(self, response):
        """
        _summary_: This function is used to parse the response from the request
        """
        # parse the response
        soup = BeautifulSoup(
            response.text.replace("<![CDATA[", "").replace("]]>", ""), "html.parser"
        )
        table = soup.find_all("table", class_="dataTable")[0]
        raw_data = table.find_all("tr")
        # pop the first row because it is the header
        raw_data.pop(0)
        # get the data
        for row in raw_data:
            data = row.find_all("td")
            yield {
                DATE: data[0].text.replace("\r\n", "").strip(),
                CLOSE_PRICE: float(
                    data[1].text.replace("\r\n", "").strip().replace(",", ".")
                ),
                TRADING_BUY_COUNT: int(
                    data[2].text.replace("\r\n", "").strip().replace(".", "")
                ),
                TRADING_BUY_VOLUME: float(
                    data[3]
                    .text.replace("\r\n", "")
                    .strip()
                    .replace(".", "")
                    .replace(",", ".")
                ),
                TRADING_SELL_COUNT: int(
                    data[4].text.replace("\r\n", "").strip().replace(".", "")
                ),
                TRADING_SELL_VOLUME: float(
                    data[5]
                    .text.replace("\r\n", "")
                    .strip()
                    .replace(".", "")
                    .replace(",", ".")
                ),
                BUY_SELL_DIFFERENCE: float(
                    data[6]
                    .text.replace("\r\n", "")
                    .strip()
                    .replace(".", "")
                    .replace(",", ".")
                ),
                AUCTION_VOLUME: float(
                    data[7]
                    .text.replace("\r\n", "")
                    .strip()
                    .replace(".", "")
                    .replace(",", ".")
                ),
                AUCTION_VALUE: float(
                    data[8]
                    .text.replace("\r\n", "")
                    .strip()
                    .replace(".", "")
                    .replace(",", ".")
                ),
            }

        # if raw_data is not empty, then we try to get the next page
        if len(raw_data) > 0:
            self.page_number += 1
            headers, payload = self.get_request_dependencies(self.page_number)
            yield Request(
                url=self.start_urls[0],
                headers=headers,
                body=payload,
                callback=self.parse,
                dont_filter=True,
            )
