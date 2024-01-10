from bs4 import BeautifulSoup
import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def get_links(url):
    time.sleep(1)
    
    response = requests.get(url, headers=headers, timeout=req_time, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', {'id': 'search-result'})

    if not table:
        return None
    
    tbody = table.find('tbody')
    if not tbody:
        return None

    link_elements = tbody.find_all('a')
    if not link_elements:
        return None

    links = []
    for el in link_elements:
        links.append(el.get('href'))

    if len(links) == 0:
        return None
    
    return links

def get_contacts(url, name):
    time.sleep(1)
    response = requests.get(url, headers=headers, timeout=req_time, verify=False)
    # response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    header_element = soup.find('th', text='Наименование на рус. языке').find_next('td').text.strip()
    if header_element:
        rus_name = header_element.find_next('td').text.strip()
        if rus_name.casefold() == name:
            email = soup.find('th', text='E-Mail:').find_next('td').text.strip()
            phone = soup.find('th', text='Контактный телефон:').find_next('td').text.strip()
            if email or phone:
                data = f'{email} {phone}'
                return data
            return None
        else:
            return None
    else:
        return None

def find_name(name):
    mappings = {
        "тоо": "товарищество с ограниченной ответственностью",
        "товарищество с ограниченной ответственностью": "тоо",
        "ао": "акционерное общество",
        "акционерное общество": "ао",
    }

    name_lower = name.lower()

    for key, value in mappings.items():
        if key.lower() in name_lower:
            return name_lower.replace(key.lower(), value)

    return None

def find_contacts(links, name, another_name):
    contacts = ''
    if links is not None:
        for link in links:
            contacts = get_contacts(link, name.casefold())
            if contacts is not None:
                return contacts
            else:
                contacts = get_contacts(link, another_name.casefold())
                if contacts is not None:
                    return contacts
        return contacts

req_time = 5000
file_path = "input/names.txt"
lines = []

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        lines.append(line.strip())

with open('output/goszakup.txt', 'w', encoding='utf-8') as file:
    for name in lines:
        print('\n') 
        another_name = find_name(name.casefold())
        url = f"https://procurement.gov.kz/ru/registry/supplierreg?filter%5Bname%5D={name}&search=&filter%5Battribute%5D="
        links = get_links(url)
        contacts = find_contacts(links, name, another_name)
        if contacts != None:
            file.write(str(contacts) + '\n')
        elif contacts == None:
            url = f"https://procurement.gov.kz/ru/registry/supplierreg?filter%5Bname%5D={another_name}&search=&filter%5Battribute%5D="
            links = get_links(url)
            contacts = find_contacts(links, name, another_name)
            file.write(str(contacts) + '\n')
        else:
            file.write(str(None) + '\n')
        print(contacts)
        print('\n')

    file.close()