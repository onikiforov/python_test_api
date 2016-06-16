from base_api import BaseApi
import xmltodict
import requests


class TestGetInfoForCurrentUser(BaseApi):

    def test_get_info_for_current_user(self):
        url = self.base_url + '/user/current'

        r = self.request(url, 'get')
        self.log_full(r)

        response_dict = xmltodict.parse(r.text)

        self.assert_basic(r, 200, 'application/xml;charset=UTF-8')
        self.assertTrue(response_dict['user']['@email'])
        self.assertTrue(response_dict['user']['@fullName'])

    def test_get_info_for_current_user_without_credentials(self):
        url = self.base_url + '/user/current'

        r = requests.get(url)
        self.log_full(r)

        self.assert_basic(r, 200, 'application/xml;charset=UTF-8')

        response_dict = xmltodict.parse(r.text)

        self.assertTrue(response_dict['user'])
        self.assertEqual(response_dict['user']['@login'], '<no user>')
        self.assertEqual(response_dict['user']['@guest'], 'false')
