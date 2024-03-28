import requests
from bs4 import BeautifulSoup
import re
import json


def fetch_search_results(keyword):
    keyword_encoded = requests.utils.quote(keyword)
    search_url = f'https://www.btnull.org/s/1---1/{keyword_encoded}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Cookie': "BT_auth=624ewAkQxIwTKTtPmao6nI1rJ4veHwI2ioLIlLzGGlnQvbAhsDYKDKgz3IgOiYM9HsskZtFlSlXo5pfjAfD5QijbGw1EAwllBp9dY7ZTrFu1RNCB49DFvdCfbCqVWUe1vaXTj5y34IZzT-gabeseFkuq_Ohv4Lsc1SRuHfm4EBg; BT_cookietime=2497lwEXti5x8jxGdM90ZT6NBTVrgcKv5H5vSDrWu4YdS4FU5pvK; vrg_go=1; vrg_sc=a0f74fadd47b1c1bebc195569da5a95d",
    }

    search_response = requests.get(search_url, headers=headers)
    search_results = []
    if search_response.status_code == 200:
        soup = BeautifulSoup(search_response.content, 'html.parser')
        for item in soup.find_all('div', class_='v5d')[:2]:  # 仅处理前3个结果
            title_link = item.find('a', class_='d16')
            img_link = item.find('img', class_='lazy')['data-src'] if item.find('img', class_='lazy') else None
            if title_link and img_link:
                movie_url = f"https://www.btnull.org{title_link['href']}"
                movie_url = movie_url.replace('.html', '')
                cover_url = img_link  # 直接使用WebP格式的封面图URL
                search_results.append({'detail_url': movie_url, 'cover_url': cover_url})
    return search_results


def fetch_movie_details_from_btnull(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Cookie': "BT_auth=624ewAkQxIwTKTtPmao6nI1rJ4veHwI2ioLIlLzGGlnQvbAhsDYKDKgz3IgOiYM9HsskZtFlSlXo5pfjAfD5QijbGw1EAwllBp9dY7ZTrFu1RNCB49DFvdCfbCqVWUe1vaXTj5y34IZzT-gabeseFkuq_Ohv4Lsc1SRuHfm4EBg; BT_cookietime=2497lwEXti5x8jxGdM90ZT6NBTVrgcKv5H5vSDrWu4YdS4FU5pvK; vrg_go=1; vrg_sc=a0f74fadd47b1c1bebc195569da5a95d",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pattern = re.compile(r'_obj\.d\s*=\s*(\{.*?\});', re.S)
        matches = pattern.search(response.text)
        if matches:
            data = json.loads(matches.group(1))
            douban_id = data.get('pf', {}).get('db', {}).get('id', '')
            douban_rating = data.get('pf', {}).get('db', {}).get('s', '')
            douban_url = f'https://movie.douban.com/subject/{douban_id}/'
            description = data.get('introduce', '').replace('\n', ' ')
            movie_details = {
                'title': data.get('title', ''),
                'year': data.get('year', ''),
                'director': data.get('daoyan', []),
                'actors': data.get('zhuyan', []),
                'category': data.get('leixing', []),
                'country': data.get('diqu', []),
                'release_date': data.get('stime', ''),
                'description': description,
                'ratings': douban_rating,
                'douban_url': douban_url
            }
            return movie_details
    return {}


def fetch_btnull_data(keyword):
    search_results = fetch_search_results(keyword)
    all_movie_details = []
    for item in search_results:
        url = item['detail_url']
        details = fetch_movie_details_from_btnull(url)
        details.update({
            'detail_url': url,  # 把详情页的URL添加到字典中
            'cover_url': item['cover_url']  # 添加封面图URL
        })
        all_movie_details.append(details)
    return all_movie_details


