from behave import given, when, then

@given('a user')
def impl(context):
    from django.contrib.auth.models import User
    u = User(username='foo', email='foo@example.com') # User u = new User()
    u.set_password('bar')

@given(u'a project')
def impl(context):
    assert False


@then(u'I see list of project in assign by me')
def impl(context):
    assert False
