import requests
from bs4 import BeautifulSoup  # use this to parse data out of HTML
import json
import time
import csv
import pandas


class ZScraper():
    results = []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'zgcus_lbut=; zgcus_aeut=146648065; zgcus_ludi=d01e1c1f-799a-11ea-aac0-0e4403354070-14664; G_ENABLED_IDPS=google; userid=X|3|674cf606c44da52a%7C7%7CUz-pb9x8hy-UN21FNiFYpusf2rp9YACM; loginmemento=1|d0c68b0822ab093a9f3407ec89cf0527a2e3e7f95a1469e53b80b53d34e1046a; zguid=24|%241eb11e00-b43f-4986-a0ad-55e439bd87a2; zgsession=1|008fdfd2-68ca-43da-8e90-195e6a3faf74; JSESSIONID=3DEDF9A629EECD6D9306A789910531EF; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEjNYDfs%2Ft92lll7LyXVKLgkgfYK3u49g2iMkg3pL9paISVA11ksMdgMr3mC34OYbcEWsuztEKCmz; search=6|1667610196905%7Cregion%3Dyork-county-va%26rect%3D37.380139%252C-76.13552%252C37.091894%252C-76.755511%26disp%3Dmap%26mdm%3Dauto%26sort%3Dpriorityscore%26fs%3D0%26fr%3D1%26mmm%3D0%26rs%3D0%26ah%3D0%09%09345%09%09%09%09%09%09; AWSALB=bEastD52P+ghHzkyGk8ah4UBDjBqd44bjl1XCS7mUqG6TfmALRuuWptJwEB/Ww5GpJGuEWGwbVKwsR0mzpm8lXzDP97i4VvBZ7iam9B4iBnGLFpZ92+ZQmPI+efO; AWSALBCORS=bEastD52P+ghHzkyGk8ah4UBDjBqd44bjl1XCS7mUqG6TfmALRuuWptJwEB/Ww5GpJGuEWGwbVKwsR0mzpm8lXzDP97i4VvBZ7iam9B4iBnGLFpZ92+ZQmPI+efO',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate,',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'

    }

    def fetch(self, url):
        response = requests.get(url, headers=self.headers)
        # no params, params=params needed
        return response

    # allows us to pull data out of HTML
    def parse(self, response):
        self.results.clear()
        content = BeautifulSoup(response)
        deck = content.find('ul', {'class': "List-c11n-8-73-8__sc-1smrmqp-0 srp__sc-1psn8tk-0 bfcHMx photo-cards with_constellation"})
        for card in deck.contents:
            # div_details = card.find('div', {'class': 'StyledPropertyCardDataWrapper-c11n-8-73-8__sc-1omp4c3-0 gXNuqr property-card-data'})
            script_details = card.find('script', {'type': 'application/ld+json'})
            if script_details:
                # price = div_details.contents[2].text
                # print(price)
                script_json = json.loads(script_details.contents[0])

                self.results.append({
                    'address': script_json['name'],
                    # 'bedrooms': card.find('span', {'class': 'StyledPropertyCardHomeDetails-c11n-8-73-8__sc-1mlc4v9-0 jlVIIO'}).text,
                    'square footage': script_json['floorSize']['value'],
                    'price': card.find('div', {'class': 'StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0 hRqIYX'}).text,
                    'url': script_json['url']

                })

        # print(self.results)

    # def to_csv(self):
    #     with open('zillow.csv', 'w') as csv_file:
    #         writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
    #         writer.writeheader()
    #
    #         for row in self.results:
    #             writer.writerow(row)

    def run(self, val):
        url = "https://www.zillow.com/homes/for_rent/"
        zip_code = val
        # params = {
        #     'searchQueryState': '{"pagination":{},"mapBounds":{"north":37.168389,"east":-76.394529,"south":37.091954,"west":-76.506101},"isMapVisible":false,"filterState":{"fore":{"value":false},"mf":{"value":false},"auc":{"value":false},"nc":{"value":false},"fr":{"value":true},"land":{"value":false},"manu":{"value":false},"fsbo":{"value":false},"cmsn":{"value":false},"fsba":{"value":false}},"isListVisible":true,"regionSelection":[{"regionId":67796,"regionType":7}]}'
        # }

        res = self.fetch(url+zip_code) # no params needed
        self.parse(res.text)
        # self.to_csv()
        df = pandas.DataFrame(self.results)
        # df.to_csv("results.csv")
        return df
        # time.sleep(2)


if __name__ == '__main__':
    scraper = ZScraper()
    scraper.run()