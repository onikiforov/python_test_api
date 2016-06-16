from base_api import BaseApi
import xmltodict
import datetime
import requests


class TestUpdateIssue(BaseApi):

    def test_update_issue(self):
        issue_id = self._create_issue()  # obviously we need to create an issue before updating it

        url = self.base_url + '/issue/' + issue_id

        current_time = str(datetime.datetime.now())[0:-7]

        issue_summary = 'Summary updated at ' + current_time
        issue_description = 'Description updated at ' + current_time

        params = {
            'summary': issue_summary,
            'description': issue_description
        }

        r = self.request(url, 'post', params)
        self.log_full(r)

        self.assert_basic(r, 200, 'text/plain;charset=UTF-8')

        url = self.base_url + '/issue/' + issue_id
        r = self.request(url, 'get')
        self.log_full(r)

        response_dict = xmltodict.parse(r.text)

        self.assert_basic(r, 200, 'application/xml;charset=UTF-8')

        self.assertEqual(response_dict['issue']['@id'], issue_id)
        for field in response_dict['issue']['field']:
            if field['@name'] == 'summary':
                self.assertEqual(field['value'], issue_summary)
            if field['@name'] == 'description':
                self.assertEqual(field['value'], issue_description)

    def test_update_not_existing_issue(self):
        url = self.base_url + '/issue/' + 'kjhfkaskafk'

        current_time = str(datetime.datetime.now())[0:-7]

        issue_summary = 'Summary updated at ' + current_time
        issue_description = 'Description updated at ' + current_time

        params = {
            'summary': issue_summary,
            'description': issue_description
        }

        r = self.request(url, 'post', params)
        self.log_full(r)

        response_dict = xmltodict.parse(r.text)

        self.assert_basic(r, 404, 'application/xml;charset=UTF-8')
        self.assertTrue(response_dict['error'])

    def test_update_issue_without_credentials(self):
        issue_id = self._create_issue()
        url = self.base_url + '/issue/' + issue_id

        current_time = str(datetime.datetime.now())[0:-7]

        issue_summary = 'Summary updated at ' + current_time
        issue_description = 'Description updated at ' + current_time

        params = {
            'summary': issue_summary,
            'description': issue_description
        }

        r = requests.post(url, params)
        self.log_full(r)

        self.assert_basic(r, 401, 'application/xml;charset=UTF-8')

        response_dict = xmltodict.parse(r.text)

        self.assertTrue(response_dict['error'])
