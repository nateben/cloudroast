__author__ = 'paul-lodronio'

from test_repo.database.fixtures import DBaaSFixture
from test_repo.database import dbaas_util as testutil


class test_actions(DBaaSFixture):

    instance_id = None
    dbaas = None

    @classmethod
    def setUpClass(cls):
        """
        Creating an instance for database testing

        """
        tc_name = "Create Instance"
        super(test_actions, cls).setUpClass()
        cls.mgmt_dbaas = cls.dbaas_provider.mgmt_client.reddwarfclient
        cls.mgmt_dbaas.authenticate()

        NAME = "qe-mgmt-actions-testing"
        FLAVOR = 1
        VOLUME = 1
        instance = test_actions.mgmt_dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME})
        httpCode = testutil.get_last_response_code(test_actions.mgmt_dbaas)
        if httpCode != '200':
            raise Exception("Create instance failed with code %s" % httpCode)
        cls.instance_id = instance.id
        cls.instance = instance
        #status = instance.status
        testutil.waitForActive(test_actions.mgmt_dbaas,
                               instanceId=test_actions.instance_id)

        #instance_details = test_actions.mgmt_dbaas.management.show( \
        #                                                            instance)
        #httpCode = testutil.get_last_response_code(test_actions.mgmt_dbaas)
        #if httpCode != '200':
        #    raise Exception("List instance details failed with code %s" %
        #                    httpCode)
        #cls.host = instance_details.server["host"]

    @classmethod
    def tearDownClass(cls):
        """
        Tearing down: Deleting the instance if in active state

        """
        # Delete the instance ID created for test if active
        if test_actions.instance_id is not None:
            status = testutil.getInstanceStatus(test_actions.mgmt_dbaas,
                                        instanceId=test_actions.instance_id)
            if testutil.isInstanceActive(test_actions.mgmt_dbaas,
                                        instanceStatus=status):
                test_actions.mgmt_dbaas.instances.get( \
                                        test_actions.instance_id).delete()

    @classmethod
    def setUp(cls):
        """
        Run this setup for each test to ensure an active instance is available

        """
        tc_name = "Create Instance"
        instance_status = testutil.getInstanceStatus(cls.mgmt_dbaas,
                                                instanceId=cls.instance_id)
        if (testutil.isInstanceActive(cls.mgmt_dbaas,
                                    instanceStatus=instance_status) is False):
            # delete non-Active instance
            test_actions.mgmt_dbaas.instances.get(cls.instance_id).delete()
            # start a new instance and set the global instance ID
            NAME = "qe-mgmt-actions-testing"
            FLAVOR = 1
            VOLUME = 1
            try:
                instance = cls.mgmt_dbaas.instances.create(
                    name=NAME,
                    flavor_id=FLAVOR,
                    volume={"size": VOLUME},
                    databases=[{"databases": [{"name": "databaseA"}],
                                "name": "dbuser1",
                                "password": "password"}])
                httpCode = testutil.get_last_response_code(cls.mgmt_dbaas)
                if httpCode != '200':
                    raise Exception("Create instance failed with code %s" %
                                    (httpCode))
                cls.instance_id = instance.id
                cls.instance = instance
                testutil.waitForActive(cls.mgmt_dbaas,
                                       instanceId=cls.instance_id)
            except Exception as e:
                self.fixture_log.debug("\tException: %r" % (e))
                raise

    def test_reboot_instance(self):
        expected_status = "REBOOT"
        expected_status_found = False
        expected_task_desc = "No tasks for the instance."
        initial_updated = ""

        # list instance details and store updated time value
        instance_details = test_actions.mgmt_dbaas.management.show( \
                                                                self.instance)
        httpCode = testutil.get_last_response_code(test_actions.mgmt_dbaas)
        if httpCode != '200':
            raise Exception("List instance details failed with code %s" %
                            httpCode)
        initial_updated = instance_details.updated
        self.fixture_log.debug("\t\tInstance %r initial update on %r" %
                               (instance_details.id, initial_updated))

        # call reboot instance
        try:
            self.mgmt_dbaas.management.reboot(self.instance_id)
            httpCode = testutil.get_last_response_code(self.mgmt_dbaas)
            self.assertTrue(httpCode == '202',
                            "Reboot instance failed with code %s" %
                            httpCode)
        except Exception as e:
            self.fixture_log.debug("\tException: %r" % (e))
            raise

        # check instance for Reboot status
        current_status, elapsed = testutil.wait_for_status(self.mgmt_dbaas,
                                                           self.instance_id,
                                                           expected_status)
        self.fixture_log.debug("\t\tInstance status encountered: %r" %
                               (current_status))
        self.assertEqual(current_status, expected_status,
                         "Expected status %r , Actual status %r" %
                         (expected_status, current_status))
        if current_status == expected_status:
            expected_status_found = True
        self.fixture_log.debug("\t\tExpected status found? %r" %
                               (expected_status_found))

        # verify it comes up in an Active state
        status, elapsed = testutil.waitForActive(self.mgmt_dbaas,
                                                instanceId=self.instance_id)
        self.fixture_log.debug("\t\tInstance status encountered: %r" %
                               (status))
        self.assertEqual(status, 'ACTIVE',
                         "Expected status %r , Actual status %r" %
                         ('ACTIVE', status))

        # make final checks
        self.assertTrue(expected_status_found,
                        "Expected status %r was not seen!" %
                        (expected_status))
        instance_details = test_actions.mgmt_dbaas.management.show( \
                                                                self.instance)
        httpCode = testutil.get_last_response_code(test_actions.mgmt_dbaas)
        if httpCode != '200':
            raise Exception("List instance details failed with code %s" %
                            httpCode)
        self.assertTrue(initial_updated != instance_details.updated,
                        "Instance %r was not updated!" %
                        (instance_details.id))
        self.fixture_log.debug("\t\tInstance %r final update on %r" %
                               (instance_details.id, instance_details.updated))

    def test_reset_instance_task_status(self):
        pass

    def test_migrate_instance(self):
        pass
