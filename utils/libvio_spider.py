import requests
from bs4 import BeautifulSoup


def fetch_search_results_from_libvio(keyword):
    # 对关键词进行URL编码
    keyword_encoded = requests.utils.quote(keyword)
    url = f'https://www.libvio.pw/search/-------------.html?wd={keyword_encoded}&submit='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Cookie': '__51vcke__KAYKsbrG2nhi832g=d7e7a0f3-4f6c-506e-a1d8-42ecb0e3ae99; __51vuft__KAYKsbrG2nhi832g=1710632406186; recente=%5B%7B%22vod_name%22%3A%22%E6%88%91%E5%8F%98%E7%BE%8E%E7%9A%84%E9%82%A3%E5%A4%8F%E5%A4%A9%20%E7%AC%AC%E4%BA%8C%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.libvio.pw%2Fplay%2F714890057-1-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%5D; PHPSESSID=ehcj4sdo2m08ch98u0knsp74pl; __vtins__KAYKsbrG2nhi832g=%7B%22sid%22%3A%20%225b957f5c-245e-5950-91f8-0aab112f4e60%22%2C%20%22vd%22%3A%201%2C%20%22stt%22%3A%200%2C%20%22dr%22%3A%200%2C%20%22expires%22%3A%201710867479304%2C%20%22ct%22%3A%201710865679304%7D; __51uvsct__KAYKsbrG2nhi832g=9',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    detail_urls = []
    for item in soup.find_all('li', class_='col-md-6 col-sm-4 col-xs-3')[:2]:  # 仅处理前3个结果
        a_tag = item.find('a', class_='stui-vodlist__thumb')
        href = a_tag['href']
        detail_url = f'https://www.libvio.pw{href}'
        cover_url = a_tag['data-original']  # 提取封面图URL
        detail_urls.append({'detail_url': detail_url, 'cover_url': cover_url})
    return detail_urls


def fetch_movie_details_from_libvio(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Cookie': '__51vcke__KAYKsbrG2nhi832g=d7e7a0f3-4f6c-506e-a1d8-42ecb0e3ae99; __51vuft__KAYKsbrG2nhi832g=1710632406186; recente=%5B%7B%22vod_name%22%3A%22%E6%88%91%E5%8F%98%E7%BE%8E%E7%9A%84%E9%82%A3%E5%A4%8F%E5%A4%A9%20%E7%AC%AC%E4%BA%8C%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.libvio.pw%2Fplay%2F714890057-1-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%5D; PHPSESSID=ehcj4sdo2m08ch98u0knsp74pl; __vtins__KAYKsbrG2nhi832g=%7B%22sid%22%3A%20%225b957f5c-245e-5950-91f8-0aab112f4e60%22%2C%20%22vd%22%3A%201%2C%20%22stt%22%3A%200%2C%20%22dr%22%3A%200%2C%20%22expires%22%3A%201710867479304%2C%20%22ct%22%3A%201710865679304%7D; __51uvsct__KAYKsbrG2nhi832g=9',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    detail_content = soup.find('div', class_='stui-content__detail')

    title = detail_content.find('h1', class_='title').text.strip()

    # 解析第一个<p class="data">
    first_data = detail_content.find_all('p', class_='data')[0].get_text(strip=True)
    info_parts = first_data.split(' /')

    # 解析并处理category
    category_raw = info_parts[0].split('：')[-1]
    category = [cat.strip() for cat in category_raw.split(',') if len(cat.strip()) > 1]

    # 解析country
    country = info_parts[1].split('：')[-1].split(',')

    # 解析release_date和year
    release_date = info_parts[3].split('：')[-1]
    year = release_date.split('-')[0]

    # 解析导演和演员
    second_data = detail_content.find_all('p', class_='data')[1].get_text(strip=True)
    actors_list = second_data.split(' /导演：')[0].replace('主演：', '').split(',')
    director = second_data.split(' /导演：')[-1]

    # 获取简介
    description = detail_content.find('span', class_='detail-sketch').text + detail_content.find('span',
                                                                                                 class_='detail-content').text

    # 获取评分和豆瓣链接
    douban_rating = detail_content.find('span', class_='douban').text.replace('分', '')
    douban_url = detail_content.find('a', href=True, title="到豆瓣页面查看")['href']

    return {
        'title': title,
        'year': year,
        'director': [director],
        'actors': actors_list,
        'category': category,
        'country': country,
        'release_date': release_date,
        'description': description,
        'ratings': douban_rating,
        'douban_url': douban_url,
        'detail_url': url
    }


def fetch_movies_data_from_libvio(keyword):
    detail_urls = fetch_search_results_from_libvio(keyword)
    movies_data = []
    for item in detail_urls:
        url = item['detail_url']
        movie_details = fetch_movie_details_from_libvio(url)
        movie_details.update({'cover_url': item['cover_url']})  # 添加封面图URL
        movies_data.append(movie_details)
    return movies_data



