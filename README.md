# Sites Monitoring Utility

The program checks the status of websites given at the input. 
Input - text file with URLs for verification. Output - the status of each site, based on the following checks:

 - the server responds to the request with the status of HTTP 200 - if its OK or Not OK;
 - the domain name of the site is paid for at least 30 days in advance;
 
 # How to launch
 
 example input
 ```
 python check_sites_health.py [filename.txt]
 ```
 
 example output
 ```
Checking https://devman.org/
HTTP Status Code: OK
Domain expires in set number of days: No
Checking https://vk.com/
HTTP Status Code: OK
Domain expires in set number of days: No
Checking https://github.com/
HTTP Status Code: OK
Domain expires in set number of days: No
```
output to nonexisting website
```
Checking https://zhukovaksusha.com/
HTTP Status Code: Not OK
No domain match for https://zhukovaksusha.com/
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
