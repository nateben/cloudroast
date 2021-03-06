import time
from datetime import datetime
from lxml import etree


path_to_report = '/var/lib/jenkins/workspace/Stability/report/report.xml'
path_to_error_report = '/var/lib/jenkins/workspace/Stability/report/error_report.xml'

# path_to_report = '/tmp/report.xml'
# path_to_error_report = '/tmp/error_report.xml'


def create_active_instance(dbaasClient,
                           name="create_active_instance",
                           flavor_id=3,
                           volume=None,
                           databases=None,
                           users=None):
    """
    Create and active instance and validate it
    :param dbaasClient:
    :param name:
    :param flavor:
    :param volume:
    :return instance_id:
    """
    if volume is None:
        volume = {"size": 2}

    instance = dbaasClient.instances.create(
        name=name,
        flavor_id=flavor_id,
        volume=volume,
        databases=databases,
        users=users
    )
    httpCode = get_last_response_code(dbaasClient)
    if httpCode != '200':
        raise Exception("Create instance failed with code %s" % httpCode)
    instance_id = instance.id
    status, elapsed_time = waitForActive(dbaasClient, instanceId=instance_id)
    if status == "ACTIVE":
        return instance_id, elapsed_time
    else:
        raise BaseException


def create_perf_instance(dbaas, flavorSize=3, volumeSize=2):

    NAME = "create_perf_instance"
    FLAVOR = flavorSize
    VOLUME = volumeSize
    _db_name1 = "perfDB"
    _databases = [{"name": _db_name1}]
    _users = [{"name": "perfUser",
               "password": "password2",
               "databases": _databases}]
    instance = dbaas.instances.create(
        name=NAME,
        flavor_id=FLAVOR,
        volume={"size": VOLUME},
        users=_users,
        databases=_databases)
    httpCode = get_last_response_code(dbaas)
    if httpCode != '200':
        raise Exception("Create instance failed with code %s" % httpCode)
    instance_id = instance.id
    waitForActive(dbaas, instanceId=instance_id)
    return instance_id


def write_to_error_report(instanceId, exceptionMsg):

    instanceId = instanceId
    exception_msg = exceptionMsg

    try:
        open(path_to_error_report)
    #Create new report
    except:
        with open(path_to_error_report, 'w') as error_report_xml:
            error_report_header = etree.Element("error_details")
            error_report_xml.write(etree.tostring(error_report_header,
                                                  pretty_print=True))
    
    #Append to report
    try:
        parser = etree.XMLParser(remove_blank_text=True) 
        tree = etree.parse(path_to_error_report, parser)
        error_header_root = tree.getroot()
        instanceId_element = etree.SubElement(error_header_root, "Instance", Id = instanceId)
        etree.SubElement(instanceId_element, "exception_msg").text = exception_msg
        
        with open (path_to_error_report, 'w') as error_report_xml:
            error_report_xml.write(etree.tostring(tree,
                                                  pretty_print=True))
    except Exception as err:
        print (err)
        return False    
    return True   


def write_to_report(tc_name, tc_pass=False):
    
    #Parse report to get root node
    try:
        open(path_to_report)
    except:
        with open(path_to_report, 'w') as report_xml:
            sbt_report_header = etree.Element("scenario_based_test")
            report_xml.write(etree.tostring(sbt_report_header,
                                            pretty_print=True))    
    try:
        parser = etree.XMLParser(remove_blank_text=True) 
        tree = etree.parse(path_to_report, parser)
        
        #Check to see if this test case exists
        tc_name_element_list = []
        try:
            tc_name_element_list = tree.xpath('//test_case[@name="' + tc_name + '"]')
        except Exception as err:
            print (err)
            #we didn't find the test case
            pass
        
        if len(tc_name_element_list) < 1:
            #create test case xml report block
            #scenario_based_test_tag = tree.Element('scenario_based_test')
            scenario_based_test_tag = tree.getroot()
            test_case_element = etree.SubElement(scenario_based_test_tag,"test_case", name=tc_name)
             
            if tc_pass:
                pass_num = etree.SubElement(test_case_element, "pass")
                pass_num.text = "1"
                fail_num = etree.SubElement(test_case_element, "fail")
                fail_num.text = "0"
            else:
                pass_num = etree.SubElement(test_case_element, "pass")
                pass_num.text = "0"
                fail_num = etree.SubElement(test_case_element, "fail")
                fail_num.text = "1"
            
        else:
            tc_result_element = None
            result_total = 0
                
            if tc_pass:
                tc_result_element = tree.xpath('//test_case[@name="' + tc_name + '"]/pass')[0]
                result_total = int(tree.xpath('//test_case[@name="' + tc_name + '"]/pass/text()')[0])
                #DEBUG: print ("Old Pass total = {0}".format(passTotal))
                #DEBUG: print ("New Pass total = {0}".format(passTotal))
            else:
                tc_result_element = tree.xpath('//test_case[@name="' + tc_name + '"]/fail')[0]
                result_total = int(tree.xpath('//test_case[@name="' + tc_name + '"]/fail/text()')[0])
                            
            result_total += 1    
            tc_result_element.text = str(result_total)
             
        #Write all the changes out to file
        #TODO: Copy file before writing to it in case of error        
        with open (path_to_report, 'w') as f:
                    f.write(etree.tostring(tree, pretty_print=True))
    except (Exception) as err:
        print (err)
        return False    
    return True


def wait_for_all_active(dbaasClient, inst_id_list):
    """
    :param dbaasClient:
    :param inst_id_list:
    :return:
    """
    for each_id in inst_id_list:
        waitForActive(dbaasClient, each_id)
    return True


def waitForActive(dbaasClient, instanceId=None):
    """ Waiting for 'ACTIVE' status """
    status, elapsed_time = wait_for_status(dbaasClient, instanceId, "ACTIVE")
    return status, elapsed_time


def wait_for_status(dbaasClient, instanceId, status):
    """ Waiting for passed-in status
    :rtype : status
    :rtype : elapsed_time
    @param dbaasClient:
    @param instanceId:
    @param status:
    """
    #print("Waiting for status %r on instance id: %r" % (status, instanceId))
    elapsed = 0
    startTime = time.time()
    while elapsed < 300:
        current_status = getInstanceStatus(dbaasClient, instanceId=instanceId)
        #print("Elapsed: %2.1f seconds, Status: %s" % (elapsed, current_status))
        if current_status == status:
            return current_status, elapsed
        elif current_status == "ACTIVE":
                return "ACTIVE", elapsed
        elif current_status == "ERROR" or current_status == "FAILED":
                return "ERROR", elapsed
        else:
            time.sleep(10)
            elapsed = (time.time() - startTime)
    return current_status, elapsed


def isInstanceActive(dbaasClient, instanceStatus=None, instanceId=None):
    if instanceStatus is not None:
        return instanceStatus == 'ACTIVE'
    if instanceId is not None:
        return getInstanceStatus(dbaasClient, instanceId=instanceId) == 'ACTIVE'
    return False


def getInstanceStatus(dbaasClient, instanceId=None):
    _instance = dbaasClient.instances.get(instanceId)
    return _instance.status


def getInstanceHostname(dbaasClient, instanceId=None):
    _instance = dbaasClient.instances.get(instanceId)
    return _instance.hostname


def get_last_response_code(dbaas):
    resp, body = dbaas.client.last_response
    return str(resp.status)


def valid_duration(expected_timedelta, single_event, dateFormat):
    """Returns true if the event timedelta (endTime-startTime) is
    approximate to expected_timedelta (within error_margin_timedelta);
    expected_timedelta and error_margin_timedelta are timedelta objects"""

    error_margin_timedelta = 60
    startTimeStamp = datetime.strptime(single_event.startTime, dateFormat)
    endTimeStamp = datetime.strptime(single_event.endTime, dateFormat)
    event_delta = endTimeStamp - startTimeStamp

    #print("AH recorded time: %r" % event_delta.seconds)
    #print("Live test duration: %r" % expected_timedelta.seconds)
    return abs(event_delta.seconds - expected_timedelta.seconds) <= error_margin_timedelta


def found_resource(dbaas, instanceId=None, databaseName=None, userName=None, limit=1):
    """
    This method will run pagination every time since it
    limits its reply to 1 instance per list

    @param dbaas:
    @param instanceId:
    @return: True if instance is found
    """
    instance_id = instanceId

    if databaseName:
        paginated_dbs = dbaas.databases.list(instance_id, limit=limit)
        assert (len(paginated_dbs) <= limit)
        foundDB = False
        for _db in paginated_dbs:
            #print ("Instance id found: {0}".format(instanceId))
            if _db.name == databaseName:
                #print ("Found instance with id {0}".format(_instance.id))
                foundDB = True
                break
                #Check for pagination logic
        if foundDB is False:
            next_marker = paginated_dbs.next
            while next_marker is not None:
                limit *= 2
                paginated_dbs = dbaas.databases.list(instance_id,
                                                     marker=next_marker,
                                                     limit=limit)
                for _db in paginated_dbs:
                    #print ("Instance id found: {0}".format(_instance.id))
                    if _db.name == databaseName:
                        #print ("Found instance with id {0}".format(_instance.id))
                        foundDB = True
                        break
                if foundDB is False:
                    next_marker = paginated_dbs.next
                else:
                    break
        return foundDB
    if userName:
        paginated_users = dbaas.users.list(instance_id, limit=limit)
        #TODO: put this assert back when pagination works
        assert (len(paginated_users) <= limit)
        foundUser = False
        for _user in paginated_users:
            #print ("Instance id found: {0}".format(instanceId))
            if _user.name == userName:
                #print ("Found instance with id {0}".format(_instance.id))
                foundUser = True
                break
                #Check for pagination logic
        if foundUser is False:
            next_marker = paginated_users.next
            while next_marker is not None:
                limit *= 2
                paginated_users = dbaas.users.list(instance_id,
                                                   marker=next_marker,
                                                   limit=limit)
                for _user in paginated_users:
                    #print ("Instance id found: {0}".format(_instance.id))
                    if _user.name == userName:
                        #print ("Found instance with id {0}".format(_instance.id))
                        foundUser = True
                        break
                if foundUser is False:
                    next_marker = paginated_users.next
                else:
                    break
        return foundUser
    if instanceId:
        paginated_instances = dbaas.instances.list(limit=limit)
        #TODO: put this assert back when pagination works
        assert (len(paginated_instances) <= limit)
        foundInstance = False
        for _instance in paginated_instances:
            #print ("Instance id found: {0}".format(instanceId))
            if _instance.id == instanceId:
                #print ("Found instance with id {0}".format(_instance.id))
                foundInstance = True
                break
            #Check for pagination logic
        if foundInstance is False:
            next_marker = paginated_instances.next
            while next_marker is not None:
                limit *= 2
                paginated_instances = dbaas.instances.list(marker=next_marker,
                                                           limit=limit)
                for _instance in paginated_instances:
                    #print ("Instance id found: {0}".format(_instance.id))
                    if _instance.id == instanceId:
                        #print ("Found instance with id {0}".format(_instance.id))
                        foundInstance = True
                        break
                if foundInstance is False:
                    next_marker = paginated_instances.next
                else:
                    break
        return foundInstance


class Requirements(object):
    """Defines requirements a test has of a user."""

    def __init__(self, is_admin, services=None):
        self.is_admin = is_admin
        self.services = services or ["reddwarf"]
        # Make sure they're all the same kind of string.
        self.services = [str(service) for service in self.services]

    def satisfies(self, reqs):
        """True if these requirements conform to the given requirements."""
        if reqs.is_admin != self.is_admin:
            return False
        for service in reqs.services:
            if service not in self.services:
                return False
        return True

    def __str__(self):
        return "is_admin=%s, services=%s" % (self.is_admin, self.services)

