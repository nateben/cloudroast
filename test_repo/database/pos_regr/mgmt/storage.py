__author__ = 'paul-lodronio'

from test_repo.database.fixtures import DBaaSFixture
from test_repo.database import dbaas_util as testutil


class test_storage(DBaaSFixture):

    mgmt_client = None

    @classmethod
    def setUpClass(cls):
        """
        Setup DBaaS client access

        """
        super(test_storage, cls).setUpClass()
        cls.mgmt_client = cls.dbaas_provider.mgmt_client.reddwarfclient
        cls.mgmt_client.authenticate()

    @classmethod
    def tearDownClass(cls):
        """
        Nothing to tear down

        """
        pass

    def test_storage_details(self):
        try:
            _storage_details = self.mgmt_client.storage.index()
            httpCode = testutil.get_last_response_code(self.mgmt_client)
            self.assertEqual(httpCode, '200',
                             "List storage details failed with %s"
                             % httpCode)
        except Exception as e:
            self.fixture_log.debug("\tException: %r" % (e))
            raise

        self.assertIs(type(_storage_details), list,
                      "Expected %r , Actual %r" %
                      (list, type(_storage_details)))
        for device in _storage_details:
            self.fixture_log.debug("\tStorage device: %r" %
                               (device))
            self.fixture_log.debug("\t\tStorage capacity: %r" %
                               (device.capacity))
            self.fixture_log.debug("\t\tStorage name: %r" %
                               (device.name))
            self.fixture_log.debug("\t\tStorage provision: %r" %
                               (device.provision))
            self.fixture_log.debug("\t\tStorage type: %r" %
                               (device.type))
            self.fixture_log.debug("\t\tStorage used: %r" %
                               (device.used))
            self.assertIs(type(device.capacity), dict,
                          "Expected %r , Actual %r" %
                          (dict, type(device.capacity)))
            for val in device.capacity.values():
                self.assertIs(type(val), float,
                              "Expected %r , Actual %r" %
                              (float, type(val)))
            self.assertIs(type(device.name), unicode,
                          "Expected %r , Actual %r" %
                          (unicode, type(device.name)))
            self.assertIs(type(device.provision), dict,
                          "Expected %r , Actual %r" %
                          (dict, type(device.provision)))
            self.assertIs(type(device.provision["available"]), float,
                          "Expected %r , Actual %r" %
                          (float, type(device.provision["available"])))
            self.assertIs(type(device.provision["percent"]), int,
                          "Expected %r , Actual %r" %
                          (int, type(device.provision["percent"])))
            self.assertIs(type(device.provision["total"]), float,
                          "Expected %r , Actual %r" %
                          (float, type(device.provision["total"])))
            self.assertIs(type(device.type), unicode,
                          "Expected %r , Actual %r" %
                          (unicode, type(device.type)))
            self.assertIs(type(device.used), float,
                          "Expected %r , Actual %r" %
                          (float, type(device.used)))
