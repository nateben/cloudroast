__author__ = 'nath5505'


# from proboscis.asserts import assert_false
# from proboscis import test
from proboscis import TestPlan

def load_tests(loader, config=None, stuff=None):

    # @test
    # def test_hi():
    #     assert_false("hi")

    from reddwarf.tests.config import CONFIG
    CONFIG.load_from_file("/Users/nath5505/dbaas/test-qa.conf")
    from proboscis.decorators import DEFAULT_REGISTRY
    plan = TestPlan.create_from_registry(DEFAULT_REGISTRY)
    return plan.create_test_suite(config, loader)

