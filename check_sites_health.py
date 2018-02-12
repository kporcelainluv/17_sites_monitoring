import sys
import requests
from datetime import datetime
import whois
import os


def load_urls_to_a_list(file_path):
    with open(file_path) as urls_lis:
        return urls_lis.read().splitlines()


def is_server_respond_ok(domain):
    try:
        response = requests.request("GET", domain)
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
        return None


def check_expiration_date(days_of_payment, exp_date, todays_date):
    days_due_expirency = abs(exp_date - todays_date).days
    return bool(days_due_expirency <= days_of_payment)


def output_link_and_status(server_respond):
    print("Checking {}".format(link))
    server_respond_text = "HTTP Status Code: {}"
    status = "OK" if server_respond else "Not OK"
    print(server_respond_text.format(status))


def output_domain_info(expires_in_num_of_days):
    domain_exp_text = "Domain expires in set number of days ({}): {}"
    respond_to_expiration = "Yes" if expires_in_num_of_days else "No"
    print(domain_exp_text.format(min_days_of_payment, respond_to_expiration))


if __name__ == "__main__":
    if len(sys.argv) == 1 or os.path.isfile(sys.argv[1]) is False:
        exit("Enter a valid txt file")
    text_file = sys.argv[1]
    links = load_urls_to_a_list(text_file)
    todays_date = datetime.now()
    min_days_of_payment = 30
    for link in links:
        server_respond = is_server_respond_ok(link)
        output_link_and_status(server_respond)
        exp_date = get_domain_expiration_date(link)
        if exp_date is None:
            print("No domain match for {}".format(link))
        else:
            expires_in_num_of_days = check_expiration_date(
                min_days_of_payment,
                exp_date,
                todays_date)
            output_domain_info(expires_in_num_of_days)
