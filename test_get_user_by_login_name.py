from base_api import BaseApi
import xmltodict
import requests


class TestGetUserByLoginName(BaseApi):

    def test_get_user_by_login_name(self):
        url = self.base_url + '/user/' + self.settings['credentials']['login']

        r = self.request(url, 'get')
        self.log_full(r)

        response_dict = xmltodict.parse(r.text)

        self.assert_basic(r, 200)
        self.assertTrue(response_dict['user'])
        self.assertTrue(response_dict['user']['@filterFolder'])
        self.assertTrue(response_dict['user']['@lastCreatedProject'])
        self.assertTrue(response_dict['user']['@login'])
        self.assertTrue(response_dict['user']['@email'])
        self.assertTrue(response_dict['user']['@fullName'])
        self.assertTrue(response_dict['user']['@guest'])

    def test_get_user_by_not_existing_login_name(self):
        url = self.base_url + '/user/' + 'smash'

        r = self.request(url, 'get')
        self.log_full(r)

        response_dict = xmltodict.parse(r.text)

        self.assert_basic(r, 403)
        self.assertTrue(response_dict['error'])

    def test_get_user_by_login_name_without_credentials(self):
        url = self.base_url + '/user/' + self.settings['credentials']['login']

        r = requests.get(url)
        self.log_full(r)

        self.assert_basic(r, 401, 'application/xml;charset=UTF-8')

        response_dict = xmltodict.parse(r.text)

        self.assertTrue(response_dict['error'])
