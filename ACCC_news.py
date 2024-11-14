import requests
from parsel import Selector
cookies = {
    '_ga': 'GA1.1.1489870566.1731580940',
    'monsido': '5281731580947515',
    '_ga_S5TGQHQ4G8': 'GS1.1.1731580939.1.1.1731582032.0.0.0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '_ga=GA1.1.1489870566.1731580940; monsido=5281731580947515; _ga_S5TGQHQ4G8=GS1.1.1731591799.3.1.1731593696.0.0.0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}
params = {
    'type': 'accc_news',
    'items_per_page': '100',
}
i=1
response = requests.get('https://www.accc.gov.au/news-centre',params=params, cookies=cookies, headers=headers)
parsed_data = Selector(response.text)
rows = parsed_data.xpath('//div[@class="view-content"]//div[@lang="en"]')
for row in rows:
    news_url = row.xpath('.//a[@class="accc-news-card__link row"]//@href').get()
    # if 'media-release' in news_url.strip():
    home_page = 'https://www.accc.gov.au'
    final_url = home_page + news_url
    news_heading = row.xpath('.//a[@class="accc-news-card__link row"]//h2//text()').get()
    news_summary = row.xpath('.//div[contains(@class,"summary")]//text()').get()

    response2 = requests.get(final_url,headers=headers, cookies=cookies)
    parsed_data2 = Selector(response2.text)
    Date_of_press_release = parsed_data2.xpath('//div[@class="field__item"]//time//text()').get()
    Release_number = parsed_data2.xpath('//h3[contains(text(), "Release number")]//following-sibling::div//text()').get().strip()
    Release_number = Release_number or 'N/A'
    Topics = parsed_data2.xpath('//*/div[@class="field__items"]/div/a/text()').getall()
    print(Topics)

    news_details = {
        "Date_of_press_release": Date_of_press_release,
        "Release_number": Release_number,
        "news_url": final_url,
        "news_heading": news_heading.strip(),
        "news_summary": news_summary.strip()
    }
    print(i,news_details)
    i+=1





