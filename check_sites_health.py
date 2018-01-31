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
        req = requests.request('GET', url)
        return req
    except requests.ConnectionError:
        return None


def get_domain_expiration_date(url):
    website_info = whois.whois(url)
    if website_info.expiration_date is None and website_info.status is None:
        return None
    elif type(website_info.expiration_date) == list:
        website_info.expiration_date = website_info.expiration_date[0]
    else:
        website_info.expiration_date = website_info.expiration_date

    return website_info.expiration_date


if __name__ == '__main__':
    if len(sys.argv) > 1:
        text_file = sys.argv[1]
        minimum_days_of_domain_payment = 30
        todays_date = datetime.now()
        links = collect_urls_to_a_list(text_file)
        for link in links:
            print(link, end=" ")
            server_respond = is_server_respond_with_200(link)
            if server_respond is None:
                print("failed to connect")
            else:
                print(server_respond, end=", ")
                exp_date = get_domain_expiration_date(link)
                if exp_date is None:
                    print('The domain does not exist, exiting...')
                else:
                    days_due_expirency = abs(exp_date - todays_date).days
                    if days_due_expirency <= minimum_days_of_domain_payment :
                        print("Domain expires in {} days".format(days_due_expirency))
                    else:
                        print("Domain lasts more than 30 days")
    else:
        print("Enter a valid txt file")
