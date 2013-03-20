from behave import given, when, then

@given('a user')
def impl(context):
    from django.contrib.auth.models import User
    u = User(username='foo', email='foo@example.com') # User u = new User()
    u.set_password('bar')


@when('I log in')
def impl(context):
    br = context.browser
    br.open(context.browser_url('/account/login/'))
    br.select_form(nr=0)
    br.form['username'] = 'foo'
    br.form['password'] = 'bar'
    br.submit()


@then('I see home page')
def impl(context):
    br = context.browser
    response = br.response()
    assert response.code == 200
    assert br.geturl().endswith('/')

