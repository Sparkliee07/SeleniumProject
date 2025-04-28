from behave import given, when, then

@given("I start the BDD test")
def step_given_start_test(context):
    print("Starting the BDD test")

@when("I execute a step")
def step_when_execute(context):
    print("Executing step")

@then("I should see the result")
def step_then_result(context):
    print("Step executed successfully!")
