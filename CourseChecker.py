#!/usr/bin/env python3
import configparser, requests
from bs4 import BeautifulSoup

class CourseChecker(object):
    COURSE_PAGE = 'https://wrem.sis.yorku.ca/Apps/WebObjects/ydml.woa/wa/DirectAction/document?name=CourseListv1'
    LOGIN_PAGE = 'https://passportyork.yorku.ca/ppylogin/ppylogin'

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(['creds.cfg'])

        # Ensure there is a username/password set up
        if not 'Site' in config:
            raise Exception('No [Site] section found')
        if not 'username' in config['Site']:
            raise Exception('No username key found')
        if not 'password' in config['Site']:
            raise Exception('No password key found')

        # Initialize vars
        self.username = config['Site']['username']
        self.password = config['Site']['password']
        self.session = requests.Session()

    # Login to PPY
    def start(self):
        # First pretend to load the course list to get the redir cookie set
        r = self.session.get(CourseChecker.COURSE_PAGE)


        # Prepare login data
        login_data = {
            'mli': self.username,
            'password': self.password,
            'dologin': 'Login'}
        soup = BeautifulSoup(r.text, 'html.parser')
        hiddens = soup.find_all("input", type="hidden")
        for tag in hiddens:
            login_data[tag['name']] = tag['value']

        # Log in and make sure it worked
        r = self.session.post(CourseChecker.LOGIN_PAGE, data=login_data)
        if not 'You have successfully authenticated' in r.text:
            raise Exception('Failed to login')

    # Scrape grades
    def get_grades(self):
        r = self.session.get(CourseChecker.COURSE_PAGE)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Get the table, make sure the data makes sense
        grades_table = soup.find_all('table', class_='bodytext')
        if len(grades_table) == 0:
            raise Exception('Table could not be found')
        if len(grades_table[0].find_all('tr')) <= 1:
            raise Exception('Table was empty')

        # Remove header row
        grades_rows = grades_table[0].find_all('tr')
        grades_rows = grades_rows[1:]

        # Go row-by-row and print out the grades
        for row in grades_rows:
            cells = row.find_all('td')
            course = cells[1].get_text()
            grade = cells[3].get_text()

            print("{:<20} => {:<5}".format(course, grade))

if __name__ == '__main__':
    site = CourseChecker()
    site.start()
    site.get_grades()
