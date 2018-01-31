# Sites Monitoring Utility

The program checks the status websites given at the input. Input - text file with URLs for verification. Output - the status of each site, based on the following checks:

 - the server responds to the request with the status of HTTP 200;
 - the domain name of the site is paid for at least 1 month in advance.
 
 # How to launch
 
 example input
 ```
 python check_sites_health.py check_website.txt
 ```
 
 example output
 ```
https://devman.org/ <Response [200]>, Domain lasts more than 30 days
https://vk.com/ <Response [200]>, Domain lasts more than 30 days
https://github.com/ <Response [200]>, Domain lasts more than 30 days
```
output to nonexisting website
```
https://zhukovaksusha.com/ failed to connect
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
