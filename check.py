#!/usr/bin/env python
import configparser, requests

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
        login_data = {'mli': self.username, 'password': self.password, 'dologin': 'Login'}

        r = self.session.post(CourseChecker.LOGIN_PAGE, data=login_data)

        if not 'You have successfully authenticated' in r.text:
            raise Exception('Failed to login')

    def get_page(self):
        r = self.session.get(CourseChecker.COURSE_PAGE)
        print(r.text)
site = CourseChecker()
site.start()
site.get_page()
