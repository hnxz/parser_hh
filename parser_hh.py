import bs4
import requests
import fake_useragent
import time
import json


def get_links(text):
    user_agent = fake_useragent.UserAgent()
    res = requests.get(
        url=f'https://spb.hh.ru/search/vacancy?text={text}&from=suggest_post&salary=&area=2&ored_clusters=true&enable_snippets=true&page=1',
        headers={'user-agent': user_agent.random}
    )
    if res.status_code != 200:
        return
    soup = bs4.BeautifulSoup(res.content, 'html5lib')
    try:
        quantity_page = int(soup.find('div', attrs={'class':'pager'}).find_all('span', recursive=False)[-1].find('a').find('span').text)
    except:
        return

    for page in range(quantity_page):
        try:
            requests.get(
                url=f'https://spb.hh.ru/search/vacancy?text={text}&from=suggest_post&salary=&area=2&ored_clusters=true&enable_snippets=true&page={page}',
                headers={'user-agent': user_agent.random}
            )
            if res.status_code != 200:
                continue
            soup = bs4.BeautifulSoup(res.content, 'html5lib')
            for link in soup.find_all('a', attrs={'class':'serp-item__title'}):
                yield f'{link.attrs["href"].split("?")[0]}'
        except Exception as e:
            print(f"{e}")
        #time.sleep(1)


def get_data(link):
    user_agent = fake_useragent.UserAgent()
    res = requests.get(
        url=link,
        headers={'user-agent': user_agent.random})
    if res.status_code != 200:
        return
    soup = bs4.BeautifulSoup(res.content, 'html5lib')
    try:
        name = soup.find(attrs={'class': 'bloko-header-section-1'}).text
    except:
        name = ''
    try:
        salary = soup.find(attrs={'class': 'bloko-header-section-2 bloko-header-section-2_lite'}).text.replace('\xa0', '')
    except:
        salary = ''
    try:
        tags = [tag.text.replace('\xa0', '') for tag in soup.find(attrs={'class': "bloko-tag-list"}).find_all(attrs={'class': 'bloko-tag bloko-tag_inline'})]
    except:
        tags = ''
    vacancy = {
        'name': name,
        'salary': salary,
        'tags': tags,
        'link on vacancy': link
    }
    return vacancy


if __name__ == '__main__':
    start_time = time.time()
    data = []
    for i in get_links('python'):
        data.append(get_data(i))
        #time.sleep(1)
        with open('vacansy.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    print(f'{(time.time()-start_time)/60} minutes was in scrapping')