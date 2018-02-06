import sys
import requests
from datetime import datetime
import whois


def load_urls_to_a_list(text_file):
    with open(text_file) as file_of_links:
        return file_of_links.read().splitlines()


def is_server_respond_ok(domain):
    try:
        response = requests.request('GET', domain)
        return response.ok
    except requests.ConnectionError:
        return None


def get_domain_expiration_date(url):
    try:
        domain_info = whois.whois(url)
        return domain_info.expiration_date[0]
    except whois.parser.PywhoisError:
        return None


def check_expir_date_from_param(days_of_payment, exp_date, todays_date):
    days_due_expirency = abs(exp_date - todays_date).days
    return bool(days_due_expirency <= days_of_payment)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        exit("Enter a valid txt file")
    text_file = sys.argv[1]
    links = load_urls_to_a_list(text_file)
    todays_date = datetime.now()
    min_days_of_payment = 30
    for link in links:
        print("Checking {}".format(link))
        if is_server_respond_ok(link):
            print("HTTP Status Code: OK")
        else:
            print("HTTP Status Code: Not OK")

        exp_date = get_domain_expiration_date(link)
        if exp_date is None:
            exit("No domain match for {}".format(link))
        expires_in_num_of_days = check_expir_date_from_param(
            min_days_of_payment,
            exp_date,
            todays_date
        )
        domain_exp_text = "Domain expires in set number of days ({}): {}"
        if expires_in_num_of_days:
            print(domain_exp_text.format(min_days_of_payment, "Yes"))
        else:
            print(domain_exp_text.format(min_days_of_payment, "No"))
