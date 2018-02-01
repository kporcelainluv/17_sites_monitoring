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


def check_server_status_code(url):
    try:
        website_header = requests.head(url)
        return website_header.status_code
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


def output_status_and_exp_date_to_console(todays_date,
                                          ok_status_code,
                                          minimum_days_of_domain_payment,
                                          server_respond,
                                          exp_date):
    if server_respond == ok_status_code:
        print("HTTP Status Code 200: The request has succeeded", end=" ")
    else:
        print("HTTP Status Code is {}".format(server_respond), end=" ")

    if exp_date is None:
        print('The domain does not exist, exiting...')
    else:
        days_due_expirency = abs(exp_date - todays_date).days
        if days_due_expirency <= minimum_days_of_domain_payment:
            print("Domain expires in {} days".format(days_due_expirency))
        else:
            print("Domain lasts more than 30 days")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        text_file = sys.argv[1]
        todays_date = datetime.now()
        links = collect_urls_to_a_list(text_file)
        ok_status_code = 200
        minimum_days_of_domain_payment = 30
        for link in links:
            print(link, end=" ")
            server_respond = check_server_status_code(link)
            if server_respond is None:
                exit("failed to connect")
            exp_date = get_domain_expiration_date(link)
            output_status_and_exp_date_to_console(todays_date,
                                                  ok_status_code,
                                                  minimum_days_of_domain_payment,
                                                  server_respond,
                                                  exp_date)

    else:
        print("Enter a valid txt file")
