from base_api import BaseApi
import xmltodict
import requests


class TestGetAccessibleProjects(BaseApi):

    def test_get_accessible_projects(self):
        url = self.base_url + '/project/all'

        r = self.request(url, 'get')
        self.log_full(r)

        self.assert_basic(r, 200, 'application/xml;charset=UTF-8')

        response_dict = xmltodict.parse(r.text)

        for x in response_dict['projects']['project']:
            self.assertTrue(x['@name'])
            self.assertTrue(x['@shortName'])

    def test_get_accessible_projects_without_credentials(self):
        url = self.base_url + '/project/all'

        r = requests.get(url)
        self.log_full(r)

        self.assert_basic(r, 401, 'application/xml;charset=UTF-8')

        response_dict = xmltodict.parse(r.text)

        self.assertTrue(response_dict['error'])
