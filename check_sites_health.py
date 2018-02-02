import sys
import requests
from datetime import datetime
import whois


def load_urls_to_a_list(text_file):
    with open(text_file) as file_of_links:
        return [(*file_of_links)]


def is_server_respond_ok(domain):
    try:
        response = requests.request('GET', domain)
        return response.ok
    except requests.ConnectionError:
        return None


def get_domain_expiration_date(url):
    try:
        domain_info = whois.whois(url)
        if type(domain_info.expiration_date) == list:
            return domain_info.expiration_date[0]
        else:
            return domain_info.expiration_date
    except whois.parser.PywhoisError:
        exit("No domain match for {}".format(url))


def check_if_expir_in_30_d(exp_date, todays_date):
    min_days_of_payment = 30
    days_due_expirency = abs(exp_date - todays_date).days
    if days_due_expirency <= min_days_of_payment:
        return True
    return False


if __name__ == '__main__':
    if len(sys.argv) == 1:
        exit("Enter a valid txt file")
    text_file = sys.argv[1]
    links = load_urls_to_a_list(text_file)
    todays_date = datetime.now()

    for link in links:
        print("Checking {}".format(link.strip()))
        if is_server_respond_ok(link):
            print("HTTP Status Code: OK")
        else:
            print("HTTP Status Code: Not OK")

        exp_date = get_domain_expiration_date(link)
        expires_in_30_days = check_if_expir_in_30_d(exp_date, todays_date)
        print("Domain expires in 30 days: {}".format(expires_in_30_days))
