from pytest_bdd import scenarios, given, then

scenarios("../features/example.feature")


@given("the project is configured")
def project_is_configured():
    assert True


@then("the test should pass")
def test_should_pass():
    assert True
