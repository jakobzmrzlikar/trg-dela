# - *- coding: utf- 8 - *-

import requests
import re
import os
import csv

from bs4 import BeautifulSoup

data_dir = 'data'
csv_filename = 'oglasi.csv'
cookies = {
    'PHPSESSID': '0fpcn2kjres6ffcj1sgo7754b1',
    '__cfduid': 'da7493b43f976b2312adaeacf78b4cf5a1570282673',
    '_fbp': 'GA1.2.1050972315.1570282676',
    '_gid': 'GA1.2.1291623894.1572799243',
    'pageType': 'studenti',
    'pollCookie': '15213306'
    }


def download_url_to_string(url):
    '''This function takes a URL as argument and tries to download it
    using requests. Upon success, it returns the page contents as string.'''
    try:
        # del kode, ki morda sproži napako
        r = requests.post(url, cookies=cookies)
        r.encoding = 'UTF-8'
    except requests.exceptions.ConnectionError:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print(f"failed to connect to url {url}")
        return
    # nadaljujemo s kodo če ni prišlo do napake
    if r.status_code == requests.codes.ok:
        print(f"connected succesfully to {url}")
        return r.text
    else:
        print(f"failed to download url {url}")
        return


def save_string_to_file(text, directory, filename):
    '''Write "text" to the file "filename" located in directory "directory",
    creating "directory" if necessary. If "directory" is the empty string, use
    the current directory.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    print(f"saved string to {directory}/{filename}")
    return None


def read_file_to_string(directory, filename):
    '''Return the contents of the file "directory"/"filename" as a string.'''
    path = os.path.join(directory, filename)
    with open(path, 'r') as file_in:
        return file_in.read()


def get_ads_from_page(directory, filename):
    text = read_file_to_string(directory, filename)
    soup = BeautifulSoup(text, 'lxml')
    return [div for div in soup.find_all('div', class_='jobItem')]
        

def save_ads_to_csv(ad_list, directory, filename):
    with open(f'{directory}/{filename}', 'a') as f:
        writer = csv.writer(f, delimiter=',')
        for ad in ad_list:
            li = ad.find_all('li')
            try:
                attributes = [
                    ad.find('span', class_='title').text.lower(), 
                    # neto €/h
                    ad.find('span', class_='postavka').text.split(' €')[0],
                    ad.find('span', class_='lokacija').text.lower(),
                    li[0].text.split(':')[1][1],            # st. prostih mest
                    li[1].text.lower().split(':')[1][1:-3], # trajanje dela
                    li[2].text.lower().split(':')[1][1:-2], # delovnik
                    li[4].text.lower().split(':')[1][1:],   # narava dela
                    ad.p.text                               # komentar
                ]
            except:
                continue
            writer.writerow(attributes)

def get_urls():
    for i in range(1, 299):

        page_url = f"https://www.studentski-servis.com/ess/prosta_dela.php?scrolltop=1&t=prostaDela2&page={i}&isci=1&d014=&kosarica=&sort=&selectorv=&selectorr=&selectors=&selectord=&hideisk=&workType=1&kljb=&hourlyRateFrom=4.13&hourlyRateTo=21&urnaPostavkaMin=4%2C13&urnaPostavkaMax=21%2C00&perpage=10&perpage=10"

        page_filename = f"prosta_dela_{i}.html"

        path = f'{data_dir}/{page_filename}'
        if not os.path.exists(path):
            text = download_url_to_string(page_url)
            save_string_to_file(text, data_dir, page_filename)


def save_all_ads():
    for i in range(1, 299):
        page_filename = f"prosta_dela_{i}.html"
        ads = get_ads_from_page(data_dir, page_filename)
        save_ads_to_csv(ads, data_dir, csv_filename)
        print(f"saved all ads from {page_filename} to {data_dir}/{csv_filename}")


if __name__ == "__main__":
    get_urls()
    save_all_ads()    
