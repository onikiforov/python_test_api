import unittest
import requests
import xmltodict
from yaml import load


class BaseApi(unittest.TestCase):

    def setUp(self):
        self.settings = load(open('conf.yaml').read())
        self.base_url = self.settings['base_url']
        self.cookies = self._login()

    def _login(self):
        url = self.base_url + '/user/login'
        params = {
            'login': self.settings['credentials']['login'],
            'password': self.settings['credentials']['password']
        }

        r = requests.post(url, data=params)

        # self.log_full(r)

        return r.cookies

    def _create_issue(self):
        url = self.base_url + '/issue'
        params = {
            'project': 'API',
            'summary': 'Generated by robots',
            'description': 'Hail the robots!'
        }

        r = requests.put(url, data=params, cookies=self.cookies)
        issue_id = r.headers['Location'].split('/')[-1]

        return issue_id

    def request(self, url, method, params=None):
        # method in ('get', 'post', 'put', 'delete')

        return getattr(requests, method)(url, data=params, cookies=self.cookies)

    def _get_accessible_projects(self):
        url = self.base_url + '/project/all'

        r = self.request(url, 'get')

        response_dict = xmltodict.parse(r.text)

        projects_list = []

        for x in response_dict['projects']['project']:
            projects_list.append(x['@shortName'])

        return projects_list

    # Logging functions

    def log(self, logger, r):
        self.logger = logger
        self.r = r

        logger.debug('============================')
        logger.debug('Request URL is: ' + str(r.request.url))
        logger.debug('Request Headers are: ' + str(r.request.headers))
        logger.debug('Request Body is: ' + str(r.request.body))
        logger.debug('============================')
        logger.debug('Response Headers are: ' + str(r.headers))
        logger.debug('Response body is: ' + r.text)

    def log_full(self, r):
        req = r.request
        """
        At this point it is completely built and ready
        to be fired; it is "prepared".

        However pay attention at the formatting used in
        this function because it is programmed to be pretty
        printed and may differ from the actual request.
        """
        print ''
        print('{}\n{}\n{}\n\n{}'.format(
            '-----------REQUEST-----------',
            req.method + ' ' + req.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))

        print ''

        print('{}\n{}\n{}\n\n{}'.format(
            '-----------RESPONSE-----------',
            r.status_code,
            '\n'.join('{}: {}'.format(k, v) for k, v in r.headers.items()),
            r.text,
        ))
        print ''

    # Assertion functions

    def assert_basic(self, r, code=None, content_type=None):
        if code:
            self.assertEquals(r.status_code, code)
        if content_type:
            self.assertEquals(r.headers['Content-Type'], content_type)