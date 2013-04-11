__author__ = 'nath5505'

import json

import httplib2

#Bring in the configs w/o creating a client
from test_repo.database.fixtures import DBaaSFixture


class TestContract(DBaaSFixture):
    #Get the auth configs

    @classmethod
    def setUpClass(cls):
        """
        Creating an instance for smoke testing

        """
        super(TestContract, cls).setUpClass()
        #cls.base_client = cls.dbaas_provider.client
        #cls.database = cls.dbaas_provider.client.reddwarfclient

    def test_accept_header(self):
        #print dir(self.base_client)

        h = httplib2.Http()
        #Get an auth token

        #print(self.config.auth)
        #print(self.config.database.tenant_id)
        #self.base_client.
        body = {"auth": {"tenantName": self.config.auth.tenant_id,
                         "passwordCredentials": {"username": self.config.auth.username,
                                                 "password": self.config.auth.api_key}}}

        url = self.config.auth.base_url + "/v2.0/tokens"

        headers = {'Content-type': 'application/json'}

        response, content = h.request(url, 'POST', headers=headers, body=json.dumps(body))

        auth_token = None
        if str(response.status) == '200':
            #Get the token:
            j = json.loads(content)
            auth_token = j['access']['token']['id']
        #print auth_token
        kwargs = {'headers': {'X-Auth-Token': auth_token}}
        dbaas_url = self.config.dbaas.host
        tenant_id = self.config.dbaas.tenant_id
        flavors_url = '/'.join([dbaas_url, tenant_id, "flavors"])
        response, content = h.request(flavors_url,
                                      'GET',
                                      **kwargs)
        self.assertTrue(str(response.status) == '200', "Got an unexpected response from server %s"
                                                       % response.status)
