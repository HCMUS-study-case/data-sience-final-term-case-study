"""
    _summary_: This spider is used to get insider actions of a company
    _library dependency_: scrapy, bs4
"""

# python libraries
import json

# scrapy libraries
from scrapy import Spider, Request

# other libraries
from bs4 import BeautifulSoup

# define properties name for data
DATE = "date"  # Ngày
SHAREHOLDER = "shareholder"  # Cổ đông
SHAREHOLDER_POS = "shareholder position"  # Chức vụ
TRADING_TYPE = "trading type"  # Loại giao dịch
SHARES = "shares"  # Cổ phần


class InsiderActionsSpider(Spider):
    name = "insider_actions"
    start_urls = ["https://www.stockbiz.vn/Stocks/API/InsiderActions.aspx"]
    custom_settings = {"ROBOTSTXT_OBEY": False}
    page_number = 1
    PAYLOAD_TEMPLATE = "Cart_ctl00_webPartManager_wp1405417359_wp2062936675_cbInsiderActions_Callback_Param={}"

    def start_requests(self):
        """
        _summary_: This function is called when the spider is opened. (activation function of the spider)
        """

        headers, payload = self.get_request_dependencies()
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
        payload = self.PAYLOAD_TEMPLATE.format(str(page))
        headers = {
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
        }
        return headers, payload

    def parse(self, response):
        """
        _summary_: This function is used to parse the response through bs4
        _param_: response: the response from the request
        _return_: yield Request or yield data
        """
        # parse the response
        soup = BeautifulSoup(
            response.text.replace("<![CDATA[", "").replace("]]>", ""), "html.parser"
        )
        table = soup.find_all("table", class_="dataTable")[0]
        raw_data = table.find_all("tr")[1:]
        for row in raw_data:
            data = row.find_all("td")

            # prepare data
            # because shareholder position is optional, we need to check if it exists
            # it is null if it has a -- value
            shareholder_pos = data[2].text.replace("\r\n", "").strip()
            shareholder_pos = shareholder_pos if shareholder_pos != "---" else None

            yield {
                DATE: data[0].text.replace("\r\n", "").strip(),
                SHAREHOLDER: data[1].text.replace("\r\n", "").strip(),
                SHAREHOLDER_POS: shareholder_pos,
                TRADING_TYPE: data[3].text.replace("\r\n", "").strip(),
                SHARES: int(
                    data[4]
                    .text.replace("\r\n", "")
                    .strip()
                    .replace(".", "")
                    .replace(",", ".")
                ),
            }

        # if raw_data is not empty, then continue to request the next page
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
