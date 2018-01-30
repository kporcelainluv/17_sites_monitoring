import sys
import requests
from datetime import datetime
import whois


def collect_urls_to_a_list(text_file):
    list_of_links = []
    with open(text_file) as file_of_links:
        for link in file_of_links:
            list_of_links.append(link.strip())
    return list_of_links


def is_server_respond_with_200(url):
    try:
        website_header = requests.head(url)
        return website_header.status_code
    except requests.ConnectionError:
        return "failed to connect"


def get_domain_expiration_date(url):
    protocol_letters = 8
    url = url[protocol_letters:].strip("/")
    w = whois.whois(url)
    if w.expiration_date and w.status == None:
        print('The domain does not exist, exiting...')
        exit()
    if type(w.expiration_date) == list:
        w.expiration_date = w.expiration_date[0]
    else:
        w.expiration_date = w.expiration_date

    return w.expiration_date


if __name__ == '__main__':
    if len(sys.argv) > 1:
        text_file = sys.argv[1]
    todays_date = datetime.now()
    links = collect_urls_to_a_list(text_file)
    for link in links:
        print(link, end=" ")
        print("HTTP status code", is_server_respond_with_200(link), end=", ")
        exp_date = get_domain_expiration_date(link)
        days_due_expirency = abs(exp_date - todays_date).days
        if days_due_expirency <= 30:
            print("Domain expires in {} days".format(days_due_expirency))
        else:
            print("Domain lasts more than 30 days")
