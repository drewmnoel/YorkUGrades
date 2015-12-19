# YorkUGrades
## What?
A quick Python script to dump your current course grades from Student Document Services!

## Why?
Mostly so you don't have to open up a browser just to check your grades I guess? You can also automate the check and send yourself an email / text when a grade changes. This is why I made this, but will probably irritate the login system at some point.

## How?
The script expects some configuration information in `creds.cfg`. Here's an example:

    [Site]
    Username: drewmnoel
    Password: hunter2

## Requirements?
Python 3 is required, with BeautifulSoup 4 and Requests
