from bs4 import BeautifulSoup
import requests
import math
import re
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

req_time = 1000

def get_page_data():
    search_header = soup.find('h3', class_="mb-4")
    if search_header:
        count_element = search_header.find_next('strong')
        count_text = count_element.get_text()
        number_of_companies = re.findall(r'\d+', count_text)
        count = int(''.join(number_of_companies))
        print("Count of companies: ", count)
        count = math.ceil(count / 10)
        print("Count of pages: ", count)
        return count
    else:
        return None

def find_element_from_one_page(soup):
    elements = soup.find_all(class_="item-list")
    words_to_remove = ["тоо", "ао", "товарищество с ограниченной ответственностью", "акционерное общество","жауапкершілігі шектеулі серіктестігі","жшс"]
    pattern = "|".join(re.escape(word) for word in words_to_remove)
    regex = re.compile(pattern, re.IGNORECASE)
    for element in elements:
        text = element.find(class_="title").get_text().strip()
        if "тоо" in name.casefold() or "товарищество с ограниченной ответственностью" in name.casefold():
            if "тоо" in text.casefold() or "товарищество с ограниченной ответственностью" in text.casefold():
                new_text = re.sub(regex, "", text)
                new_text = ' '.join(new_text.split())
                new_name = re.sub(regex, "", name)
                new_name = ' '.join(new_name.split())
                if new_text.casefold() == new_name.casefold():
                    company = {
                        'name': element.select_one('.title').get_text().strip(),
                        'link': element.select_one('a.stretched')['href']
                    }
                    return company
        elif "ао" in name.casefold() or "акционерное общество" in name.casefold():
            if "ао" in text.casefold() or "акционерное общество" in text.casefold():
                new_text = re.sub(regex, "", text)
                new_text = ' '.join(new_text.split())
                new_name = re.sub(regex, "", name)
                new_name = ' '.join(new_name.split())
                if new_text.casefold() == new_name.casefold():
                    company = {
                        'name': element.select_one('.title').get_text().strip(),
                        'link': element.select_one('a.stretched')['href']
                    }
                    return company
        elif "жшс" in name.casefold() or "жауапкершілігі шектеулі серіктестігі" in name.casefold():
            if "жшс" in text.casefold() or "жауапкершілігі шектеулі серіктестігі" in text.casefold():
                new_text = re.sub(regex, "", text)
                new_text = ' '.join(new_text.split())
                new_name = re.sub(regex, "", name)
                new_name = ' '.join(new_name.split())
                if new_text.casefold() == new_name.casefold():
                    company = {
                        'name': element.select_one('.title').get_text().strip(),
                        'link': element.select_one('a.stretched')['href']
                    }
                    return company
    return None

def get_contacts(soup):
    ul_element = soup.find(class_="list-unstyled")
    phones = ul_element.find_all(class_="phone")
    mails = ul_element.find_all(class_="mail")
    contacts = []
    for i in phones:
        contacts.append(i.find('a').get_text().strip())
    for i in mails:
        contacts.append(i.find('a').get_text().strip())
    return ', '.join(contacts)

def  find_contacts_of_company(max_page, page, url):
    if max_page != None: 
        start_time = time.time()
        while page <= max_page:

            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time >= 5:
                return 'Time out'

            response = requests.get(url, headers=headers, timeout=req_time)
            soup = BeautifulSoup(response.text, 'html.parser')
            company = find_element_from_one_page(soup)
            if company != None:
                company_link = f"https://www.enbek.kz{company['link']}"
                response_of_link = requests.get(company_link, headers=headers, timeout=req_time)
                soup_of_link = BeautifulSoup(response_of_link.text, 'html.parser')
                contacts = get_contacts(soup_of_link)
                return contacts
            url = f"https://www.enbek.kz/ru/search/pou?pou_name={name}&region_id=&type=pou&page={page}"
            page += 1
    else:
        return 'No data'
    
file_path = "input/names.txt"
lines = []
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        lines.append(line.strip())
with open('output/enbek.txt', 'w') as file:
    for name in lines:
        print(name)
        page = 1 
        url = f"https://www.enbek.kz/ru/search/pou?pou_name={name}&region_id=&type=pou&page={page}"
        response = requests.get(url, headers=headers, timeout=req_time)
        soup = BeautifulSoup(response.text, 'html.parser')
        max_page = get_page_data()
        contacts = find_contacts_of_company(max_page, page, url)
        print(contacts)
        file.write(str(contacts) + '\n')
    file.close()