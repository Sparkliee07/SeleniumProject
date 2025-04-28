from behave import *

@given(u'I navigate to application')
def step_impl(context):
    print( "Inside - I navigate to application  ")


@when(u'I enter valid product into Search box')
def step_impl(context):
    print("Inside - I enter valid product into Search box  ")



@when(u'I click on Search button')
def step_impl(context):
    print("Inside - I click on Search button  ")



@then(u'Valid product should be displayed in Search results page')
def step_impl(context):
    print("Inside - Valid product should be displayed in Search results page  ")

@when(u'I enter invalid product into Search box')
def step_impl(context):
    print("Inside - I enter invalid product into Search box")
    #raise NotImplementedError(u'STEP: When I enter invalid product into Search box')


@then(u'Proper message should be displayed in Search results page')
def step_impl(context):
    print("Inside - Proper message should be displayed in Search results page")
    #raise NotImplementedError(u'STEP: Then Proper message should be displayed in Search results page')

