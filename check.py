#!/usr/bin/env python
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

        self.username = config['Site']['username']
        self.password = config['Site']['password']
        self.session = requests.Session()

    # Login to PPY
    def start(self):
        # First pretend to load the course list
        self.session.get(CourseChecker.COURSE_PAGE)

        # Then go actually log in
        login_data = {
            'mli': self.username,
            'password': self.password,
            'dologin': 'Login'}

        r = self.session.post(CourseChecker.LOGIN_PAGE, data=login_data)

        if not 'You have successfully authenticated' in r.text:
            raise Exception('Failed to login')

    def get_grades(self):
        r = self.session.get(CourseChecker.COURSE_PAGE)
        #print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Get the table, rip into rows, nuke header row
        grades_table = soup.find_all('table', class_='bodytext')
        if len(grades_table) != 1:
            raise Exception('Table could not be found')

        grades_rows = grades_table[0].find_all('tr')
        if len(grades_rows) <= 1:
            raise Exception('Table was empty')

        grades_rows = grades_rows[1:]

        # Go row-by-row
        for row in grades_rows:
            cells = row.find_all('td')
            course = cells[1].get_text()
            grade = cells[3].get_text()

            print("{:<20} => {:<5}".format(course, grade))

site = CourseChecker()
site.start()
site.get_grades()
