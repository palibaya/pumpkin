from behave import given, when, then


@given(u'memiliki username "{username}" dan password "{password}"')
def impl(context, username, password):
    from django.contrib.auth.models import User
    u = User(username=username, email='foo@bar.com')
    u.set_password(password)


@when(u'saya membuka halaman dengan session baru')
def impl(context):
    br = context.browser
    br.get(context.browser_url('/'))

@then(u'saya akan diarahkan ke halaman login')
def impl(context):
    assert context.browser.current_url.startswith(context.browser_url('/accounts/login'))

@when(u'mengisikan username "{username}"')
def impl(context, username):
    context.browser.find_element_by_name('username').send_keys(username)

@when(u'mengisikan password "{password}"')
def impl(context, password):
    context.browser.find_element_by_name('password').send_keys(password)

@when(u'melakukan submit form')
def impl(context):
    context.browser.find_element_by_tag_name('form').submit()

@then(u'Saya akan menuju pada halaman utama')
def impl(context):
    assert context.browser.current_url.endswith('/')






