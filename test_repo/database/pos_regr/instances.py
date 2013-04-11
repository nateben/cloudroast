__author__ = 'nath5505'

from test_repo.database.fixtures import DBaaSFixture
from test_repo.database import dbaas_util as testutil


class test_create_instances(DBaaSFixture):

    instance_id = None
    tiny_instance_id = None
    sml_instance_id = None
    med_instance_id = None
    lrg_instance_id = None
    xlrg_instance_id = None
    xxlrg_instance_id = None
    multi_dbs_instance_id = None
    req_params_instance_id = None
    multi_users_instance_id = None
    all_instances = [instance_id, tiny_instance_id, sml_instance_id, med_instance_id,
                     lrg_instance_id, xlrg_instance_id, xxlrg_instance_id,
                     multi_dbs_instance_id, req_params_instance_id, multi_users_instance_id]

    dbaas = None
    stability_mode = False

    @classmethod
    def setUpClass(cls):
        """
        Creating an instance for smoke testing

        """
        tc_name = "Create Instance"
        super(test_create_instances, cls).setUpClass()
        test_create_instances.dbaas = cls.dbaas_provider.client.reddwarfclient

    @classmethod
    def tearDownClass(cls):
        """
        Tearing down: Deleting the instance if in active state

        """
        #Delete the instance ID created for test if active
        dbaas = test_create_instances.dbaas
        for instance_id in test_create_instances.all_instances:
            if instance_id is not None:
                status = testutil.getInstanceStatus(dbaas, instanceId=instance_id)
                if testutil.isInstanceActive(dbaas, instanceStatus=status):
                    dbaas.instances.get(instance_id).delete()

    @classmethod
    def tearDown(cls):
        """
        Tearing down: Deleting the instance if in active state

        """
        cls.tearDownClass()
        # #Delete the instance ID created for test if active
        # for instance in test_create_instances.all_instances:
        #     if instance is not None:
        #         status = testutil.getInstanceStatus(test_create_instances.database, instance)
        #         if testutil.isInstanceActive(test_create_instances.database, instanceStatus=status):
        #             test_create_instances.database.instances.get(instance).delete()

    # @classmethod
    # def setUp(cls):
    #     """
    #     Run this setup for each test to ensure an active instance is available
    #
    #     """
    #     tc_name = "Create Instance"
    #     if test_create_instances.instance_id is None or \
    #             testutil.isInstanceActive(test_create_instances.database, instanceStatus=testutil.getInstanceStatus(
    #                     test_create_instances.database, instanceId=test_create_instances.instance_id) is False):
    #         NAME = "qe-smoke"
    #         FLAVOR = 1
    #         VOLUME = 1
    #         try:
    #             instance = test_create_instances.database.instances.create(
    #                 name=NAME,
    #                 flavor_id=FLAVOR,
    #                 volume={"size": VOLUME},
    #                 databases=[{"databases": [{"name": "databaseA"}], "name": "dbuser1",
    #                             "password": "password"}])
    #             httpCode = testutil.get_last_response_code(test_create_instances.database)
    #             if httpCode != '200':
    #                 raise Exception("Create instance failed with code %s" % httpCode)
    #             test_create_instances.instance_id = instance.id
    #             #status = instance.status
    #             testutil.waitForActive(test_create_instances.database, instanceId=test_create_instances.instance_id)
    #             if test_create_instances.stability_mode:
    #                 testutil.write_to_report(tc_name, tc_pass=True)
    #         except Exception as e:
    #             if test_create_instances.stability_mode:
    #                 testutil.write_to_error_report(test_create_instances.instance_id, repr(e))
    #                 testutil.write_to_report(tc_name, tc_pass=False)

    def test_create_tiny_instance(self):
        """
        Creating an instance for smoke testing

        """

        #database = self.dbaas_provider.client.reddwarfclient
        NAME = "qe-tiny-instance"
        FLAVOR = 1
        VOLUME = 20
        instance = self.dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME},
            databases=[{"databases": [{"name": "databaseA"}],
                        "name": "dbuser1",
                        "password": "password"}])
        httpCode = testutil.get_last_response_code(self.dbaas)
        self.assertTrue(httpCode == '200',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(self.dbaas, instanceId=instance.id)
        self.tiny_instance_id = instance.id

        #print (self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(self.dbaas, instanceId=instance.id) == 'ACTIVE',
                        "Instance is not in Active statue")
        #Get the instance and check instance attribs: such as the flavor / volume size
        instance = self.dbaas.instances.get(instance)
        self.assertTrue(instance.flavor['id'] == str(FLAVOR))
        self.assertTrue(instance.volume['size'] == VOLUME)
        self.assertTrue(instance.name == NAME)
        #try to find our instance in the list
        self.assertTrue(testutil.found_resource(self.dbaas, instanceId=instance.id),
                        "Did not find our instance id: %s in the list." % instance.id)

    def test_create_small_instance(self):
        """
        Creating an instance for smoke testing

        """
        #print (self.instance_id)
        dbaas = self.dbaas_provider.client.reddwarfclient
        NAME = "qe-small-instance"
        FLAVOR = 2
        VOLUME = 40
        instance = dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME},
            databases=[{"databases": [{"name": "databaseA"}],
                        "name": "dbuser1",
                        "password": "password"}])
        httpCode = testutil.get_last_response_code(dbaas)
        self.sml_instance_id = instance.id
        self.assertTrue(httpCode == '200',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=instance.id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=instance.id) == 'ACTIVE',
                        "Instance is not in Active statue")

        #Get the instance and check instance attribs: such as the flavor / volume size
        instance = self.dbaas.instances.get(instance)
        self.assertTrue(instance.flavor['id'] == str(FLAVOR))
        self.assertTrue(instance.volume['size'] == VOLUME)
        self.assertTrue(instance.name == NAME)
        #try to find our instance in the list
        self.assertTrue(testutil.found_resource(self.dbaas, instanceId=instance.id),
                        "Did not find our instance id: %s in the list." % instance.id)

    def test_create_medium_instance(self):
        """
        Creating an instance for smoke testing

        """
        dbaas = self.dbaas_provider.client.reddwarfclient
        NAME = "qe-medium-instance"
        FLAVOR = 3
        VOLUME = 75
        instance = dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME},
            databases=[{"databases": [{"name": "databaseA"}],
                        "name": "dbuser1",
                        "password": "password"}])
        httpCode = testutil.get_last_response_code(dbaas)
        self.med_instance_id = instance.id
        self.assertTrue(httpCode == '200',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=instance.id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=instance.id) == 'ACTIVE',
                        "Instance is not in Active statue")

        #Get the instance and check instance attribs: such as the flavor / volume size
        instance = self.dbaas.instances.get(instance)
        self.assertTrue(instance.flavor['id'] == str(FLAVOR))
        self.assertTrue(instance.volume['size'] == VOLUME)
        self.assertTrue(instance.name == NAME)
        #try to find our instance in the list
        self.assertTrue(testutil.found_resource(self.dbaas, instanceId=instance.id),
                        "Did not find our instance id: %s in the list." % instance.id)

    def test_create_large_instance(self):
        """
        Creating an instance for smoke testing

        """
        dbaas = self.dbaas_provider.client.reddwarfclient
        NAME = "qe-large-instance"
        FLAVOR = 4
        VOLUME = 100
        instance = dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME},
            databases=[{"databases": [{"name": "databaseA"}],
                        "name": "dbuser1",
                        "password": "password"}])
        httpCode = testutil.get_last_response_code(dbaas)
        self.lrg_instance_id = instance.id
        self.assertTrue(httpCode == '200',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=instance.id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=instance.id) == 'ACTIVE',
                        "Instance is not in Active statue")

        #Get the instance and check instance attribs: such as the flavor / volume size
        instance = self.dbaas.instances.get(instance)
        self.assertTrue(instance.flavor['id'] == str(FLAVOR))
        self.assertTrue(instance.volume['size'] == VOLUME)
        self.assertTrue(instance.name == NAME)
        #try to find our instance in the list
        self.assertTrue(testutil.found_resource(self.dbaas, instanceId=instance.id),
                        "Did not find our instance id: %s in the list." % instance.id)

    def test_create_xlarge_instance(self):
        """
        Creating an instance for smoke testing

        """
        dbaas = self.dbaas_provider.client.reddwarfclient
        NAME = "qe-xlarge-instance"
        FLAVOR = 5
        VOLUME = 125
        instance = dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME},
            databases=[{"databases": [{"name": "databaseA"}],
                        "name": "dbuser1",
                        "password": "password"}])
        httpCode = testutil.get_last_response_code(dbaas)
        self.xlrg_instance_id_instance_id = instance.id
        self.assertTrue(httpCode == '200',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=instance.id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=instance.id) == 'ACTIVE',
                        "Instance is not in Active statue")

        #Get the instance and check instance attribs: such as the flavor / volume size
        instance = self.dbaas.instances.get(instance)
        self.assertTrue(instance.flavor['id'] == str(FLAVOR))
        self.assertTrue(instance.volume['size'] == VOLUME)
        self.assertTrue(instance.name == NAME)
        #try to find our instance in the list
        self.assertTrue(testutil.found_resource(self.dbaas, instanceId=instance.id),
                        "Did not find our instance id: %s in the list." % instance.id)

    def test_create_xxlarge_instance(self):
        """
        Creating an instance for smoke testing

        """
        dbaas = self.dbaas_provider.client.reddwarfclient
        NAME = "qe-xxlarge-instance"
        FLAVOR = 6
        VOLUME = 150
        instance = dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME},
            databases=[{"databases": [{"name": "databaseA"}],
                        "name": "dbuser1",
                        "password": "password"}])
        httpCode = testutil.get_last_response_code(dbaas)
        self.xxlrg_instance_id = instance.id
        self.assertTrue(httpCode == '200',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=instance.id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=instance.id) == 'ACTIVE',
                        "Instance is not in Active statue")

        #Get the instance and check instance attribs: such as the flavor / volume size
        instance = self.dbaas.instances.get(instance)
        self.assertTrue(instance.flavor['id'] == str(FLAVOR))
        self.assertTrue(instance.volume['size'] == VOLUME)
        self.assertTrue(instance.name == NAME)
        #try to find our instance in the list
        self.assertTrue(testutil.found_resource(self.dbaas, instanceId=instance.id),
                        "Did not find our instance id: %s in the list." % instance.id)

    def test_create_2_dbs_instance(self):
        """
        Creating an instance for smoke testing

        """
        dbaas = self.dbaas_provider.client.reddwarfclient
        NAME = "qe-2dbs-instance"
        FLAVOR = 1
        VOLUME = 10

        databases = []
        databases.append({"name": "firstdb",
                          "character_set": "latin2",
                          "collate": "latin2_general_ci"})
        databases.append({"name": "db2"})
        users = []
        users.append({"name": "lite",
                      "password": "litepass",
                      "databases": [{"name": "firstdb"},
                                    {"name": "db2"}]})

        instance = dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME},
            databases=databases,
            users=users)
        httpCode = testutil.get_last_response_code(dbaas)
        self.multi_dbs_instance_id = instance.id
        self.assertTrue(httpCode == '200',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=instance.id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=instance.id) == 'ACTIVE',
                        "Instance is not in Active statue")

        #Get the instance and check instance attribs: such as the flavor / volume size
        instance = self.dbaas.instances.get(instance)
        self.assertTrue(instance.flavor['id'] == str(FLAVOR))
        self.assertTrue(instance.volume['size'] == VOLUME)
        self.assertTrue(instance.name == NAME)
        #try to find our instance in the list
        self.assertTrue(testutil.found_resource(self.dbaas, instanceId=instance.id),
                        "Did not find our instance id: %s in the list." % instance.id)

    def test_create_2_users_instance(self):
        """
        Creating an instance for smoke testing

        """
        dbaas = self.dbaas_provider.client.reddwarfclient
        NAME = "qe-2users-instance"
        FLAVOR = 1
        VOLUME = 10

        databases = []
        databases.append({"name": "firstdb",
                          "character_set": "latin2",
                          "collate": "latin2_general_ci"})
        users = []
        users.append({"name": "lite",
                      "password": "litepass",
                      "databases": [{"name": "firstdb"}]})
        users.append({"name": "lite1",
                      "password": "litepass1",
                      "databases": [{"name": "firstdb"}]})

        instance = dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME},
            databases=databases,
            users=users)
        httpCode = testutil.get_last_response_code(dbaas)
        self.multi_users_instance_id = instance.id
        self.assertTrue(httpCode == '200',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=instance.id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=instance.id) == 'ACTIVE',
                        "Instance is not in Active statue")

        #Get the instance and check instance attribs: such as the flavor / volume size
        instance = self.dbaas.instances.get(instance)
        self.assertTrue(instance.flavor['id'] == str(FLAVOR))
        self.assertTrue(instance.volume['size'] == VOLUME)
        self.assertTrue(instance.name == NAME)
        #try to find our instance in the list
        self.assertTrue(testutil.found_resource(self.dbaas, instanceId=instance.id),
                        "Did not find our instance id: %s in the list." % instance.id)

    def test_create_required_params_instance(self):
        """
        Creating an instance for smoke testing

        """
        dbaas = self.dbaas_provider.client.reddwarfclient
        NAME = "qe-req-params-instance"
        FLAVOR = 1
        VOLUME = 10
        instance = dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME})
        httpCode = testutil.get_last_response_code(dbaas)
        self.req_params_instance_id = instance.id
        self.assertTrue(httpCode == '200',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=instance.id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=instance.id) == 'ACTIVE',
                        "Instance is not in Active statue")

        #Get the instance and check instance attribs: such as the flavor / volume size
        instance = self.dbaas.instances.get(instance)
        self.assertTrue(instance.flavor['id'] == str(FLAVOR))
        self.assertTrue(instance.volume['size'] == VOLUME)
        self.assertTrue(instance.name == NAME)
        #try to find our instance in the list
        self.assertTrue(testutil.found_resource(self.dbaas, instanceId=instance.id),
                        "Did not find our instance id: %s in the list." % instance.id)


class test_resize_instances(DBaaSFixture):

    instance_id = None
    dbaas = None

    class flavorTypes():
        tiny = 1
        small = 2
        med = 3
        large = 4
        xlarge = 5
        xxlarge = 6

    @classmethod
    def setUpClass(cls):
        """
        Creating an instance for smoke testing

        """
        tc_name = "Create Instance"
        super(test_resize_instances, cls).setUpClass()
        test_resize_instances.dbaas = cls.dbaas_provider.client.reddwarfclient

        NAME = "qe-resize_instances"
        FLAVOR = 1
        VOLUME = 10
        instance = test_resize_instances.dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME},
            databases=[{"databases": [{"name": "databaseA"}],
                        "name": "dbuser1",
                        "password": "password"}])
        httpCode = testutil.get_last_response_code(test_resize_instances.dbaas)
        if httpCode != '200':
            raise Exception("Create instance failed with code %s" % httpCode)
        test_resize_instances.instance_id = instance.id
        #status = instance.status
        testutil.waitForActive(test_resize_instances.dbaas, instanceId=test_resize_instances.instance_id)

    @classmethod
    def tearDownClass(cls):
        """
        Tearing down: Deleting the instance if in active state

        """
        instance_id = test_resize_instances.instance_id
        dbaas = test_resize_instances.dbaas
        #Delete the instance ID created for test if active
        if instance_id is not None:
            status = testutil.getInstanceStatus(dbaas, instanceId=instance_id)
            if testutil.isInstanceActive(dbaas, instanceStatus=status):
                dbaas.instances.get(instance_id).delete()

    def test_resize_to_med_instance(self):
        """
        Resize an instance to med

        """

        dbaas = self.dbaas_provider.client.reddwarfclient
        if testutil.isInstanceActive(dbaas, instanceId=self.instance_id):
            dbaas.instances.resize_instance(self.instance_id, self.flavorTypes.med)

        httpCode = testutil.get_last_response_code(dbaas)
        self.assertTrue(httpCode == '202',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=self.instance_id) == 'ACTIVE',
                        "Instance is not in Active statue")
        newFlavorSize = dbaas.instances.get(self.instance_id).flavor['id']
        self.assertTrue(newFlavorSize == str(self.flavorTypes.med),
                        "Unexpected flavor size for resize: %s" % newFlavorSize)

        #Resize back to tiny
        if testutil.isInstanceActive(dbaas, instanceId=self.instance_id):
            dbaas.instances.resize_instance(self.instance_id, self.flavorTypes.tiny)

        httpCode = testutil.get_last_response_code(dbaas)
        self.assertTrue(httpCode == '202',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=self.instance_id) == 'ACTIVE',
                        "Instance is not in Active statue")

    def test_resize_to_large_instance(self):
        """
        Resize the instance from to med and back to tiny

        """
        dbaas = self.dbaas_provider.client.reddwarfclient
        if testutil.isInstanceActive(dbaas, instanceId=self.instance_id):
            dbaas.instances.resize_instance(self.instance_id, self.flavorTypes.large)

        httpCode = testutil.get_last_response_code(dbaas)
        self.assertTrue(httpCode == '202',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=self.instance_id) == 'ACTIVE',
                        "Instance is not in Active statue")

        newFlavorSize = dbaas.instances.get(self.instance_id).flavor['id']
        self.assertTrue(newFlavorSize == str(self.flavorTypes.large),
                        "Unexpected flavor size for resize: %s" % newFlavorSize)

        #Resize back to tiny
        if testutil.isInstanceActive(dbaas, instanceId=self.instance_id):
            dbaas.instances.resize_instance(self.instance_id, self.flavorTypes.tiny)

        httpCode = testutil.get_last_response_code(dbaas)
        self.assertTrue(httpCode == '202',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=self.instance_id) == 'ACTIVE',
                        "Instance is not in Active statue")

    def test_resize_to_xlarge_instance(self):
        """
        Resize the instance to xlarge

        """

        dbaas = self.dbaas_provider.client.reddwarfclient
        if testutil.isInstanceActive(dbaas, instanceId=self.instance_id):
            dbaas.instances.resize_instance(self.instance_id, self.flavorTypes.xlarge)

        httpCode = testutil.get_last_response_code(dbaas)
        self.assertTrue(httpCode == '202',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=self.instance_id) == 'ACTIVE',
                        "Instance is not in Active statue")

        newFlavorSize = dbaas.instances.get(self.instance_id).flavor['id']
        self.assertTrue(newFlavorSize == str(self.flavorTypes.xlarge),
                        "Unexpected flavor size for resize: %s" % newFlavorSize)

        #Resize back to tiny
        if testutil.isInstanceActive(dbaas, instanceId=self.instance_id):
            dbaas.instances.resize_instance(self.instance_id, self.flavorTypes.tiny)

        httpCode = testutil.get_last_response_code(dbaas)
        self.assertTrue(httpCode == '202',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=self.instance_id) == 'ACTIVE',
                        "Instance is not in Active statue")

    def test_resize_to_xxlarge_instance(self):
        """
        Resize the instance to xxlarge

        """

        dbaas = self.dbaas_provider.client.reddwarfclient
        if testutil.isInstanceActive(dbaas, instanceId=self.instance_id):
            dbaas.instances.resize_instance(self.instance_id, self.flavorTypes.xxlarge)

        httpCode = testutil.get_last_response_code(dbaas)
        self.assertTrue(httpCode == '202',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=self.instance_id) == 'ACTIVE',
                        "Instance is not in Active statue")

        newFlavorSize = dbaas.instances.get(self.instance_id).flavor['id']
        self.assertTrue(newFlavorSize == str(self.flavorTypes.xxlarge),
                        "Unexpected flavor size for resize: %s" % newFlavorSize)

        #Resize back to tiny
        if testutil.isInstanceActive(dbaas, instanceId=self.instance_id):
            dbaas.instances.resize_instance(self.instance_id, self.flavorTypes.tiny)

        httpCode = testutil.get_last_response_code(dbaas)
        self.assertTrue(httpCode == '202',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=self.instance_id) == 'ACTIVE',
                        "Instance is not in Active statue")


class test_resize_volume_instances(DBaaSFixture):

    instance_id = None
    dbaas = None

    class ResizeUpSizes():
        origLevel = 10
        lev1 = 20
        lev2 = 80
        lev3 = 150

    @classmethod
    def setUpClass(cls):
        """
        Creating an instance for smoke testing

        """

        super(test_resize_volume_instances, cls).setUpClass()
        test_resize_volume_instances.dbaas = cls.dbaas_provider.client.reddwarfclient

        NAME = "qe-resize_instances"
        FLAVOR = 1
        VOLUME = test_resize_volume_instances.ResizeUpSizes.origLevel
        instance = test_resize_volume_instances.dbaas.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME},
            databases=[{"databases": [{"name": "databaseA"}],
                        "name": "dbuser1",
                        "password": "password"}])
        httpCode = testutil.get_last_response_code(test_resize_volume_instances.dbaas)
        if httpCode != '200':
            raise Exception("Create instance failed with code %s" % httpCode)
        test_resize_volume_instances.instance_id = instance.id
        #status = instance.status
        testutil.waitForActive(test_resize_volume_instances.dbaas, instanceId=test_resize_volume_instances.instance_id)

    @classmethod
    def tearDownClass(cls):
        """
        Tearing down: Deleting the instance if in active state

        """
        instance_id = test_resize_volume_instances.instance_id
        dbaas = test_resize_volume_instances.dbaas
        #Delete the instance ID created for test if active
        if instance_id is not None:
            status = testutil.getInstanceStatus(dbaas, instanceId=instance_id)
            if testutil.isInstanceActive(dbaas, instanceStatus=status):
                dbaas.instances.get(instance_id).delete()

    def test_resize_volume_instance(self):
        """
        Resize the volume of an instance

        """

        dbaas = self.dbaas_provider.client.reddwarfclient
        if testutil.isInstanceActive(dbaas, instanceId=self.instance_id):
            dbaas.instances.resize_volume(self.instance_id, self.ResizeUpSizes.lev1)

        httpCode = testutil.get_last_response_code(dbaas)
        self.assertTrue(httpCode == '202',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=self.instance_id) == 'ACTIVE',
                        "Instance is not in Active statue")
        newVolume = dbaas.instances.get(self.instance_id).volume['size']
        self.assertTrue(newVolume == self.ResizeUpSizes.lev1, "Expected new volume size %s: Got %s "
                                                              % (self.ResizeUpSizes.lev1, newVolume))

        if testutil.isInstanceActive(dbaas, instanceId=self.instance_id):
            dbaas.instances.resize_volume(self.instance_id, self.ResizeUpSizes.lev2)

        httpCode = testutil.get_last_response_code(dbaas)
        self.assertTrue(httpCode == '202',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=self.instance_id) == 'ACTIVE',
                        "Instance is not in Active statue")
        newVolume = dbaas.instances.get(self.instance_id).volume['size']
        self.assertTrue(newVolume == self.ResizeUpSizes.lev2, "Expected new volume size %s: Got %s "
                                                              % (self.ResizeUpSizes.lev2, newVolume))

        if testutil.isInstanceActive(dbaas, instanceId=self.instance_id):
            dbaas.instances.resize_volume(self.instance_id, self.ResizeUpSizes.lev3)

        httpCode = testutil.get_last_response_code(dbaas)
        self.assertTrue(httpCode == '202',
                        "Create instance failed with code %s" % httpCode)
        testutil.waitForActive(dbaas, instanceId=self.instance_id)
        self.assertTrue(testutil.getInstanceStatus(dbaas, instanceId=self.instance_id) == 'ACTIVE',
                        "Instance is not in Active statue")
        newVolume = dbaas.instances.get(self.instance_id).volume['size']
        self.assertTrue(newVolume == self.ResizeUpSizes.lev3, "Expected new volume size %s: Got %s "
                                                              % (self.ResizeUpSizes.lev3, newVolume))


