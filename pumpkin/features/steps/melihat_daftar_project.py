from behave import given, when, then

# Scenario: See list of Project

@given(u'memiliki beberapa data user')
def impl(context):
    from django.contrib.auth.models import User
    context.users = {}
    for row in context.table:
        if row['is_admin'] == '1':
            u = User.objects.create_superuser(row['username'],
                                              row['email'],
                                              row['password'])
        else:
            u = User(username=row['username'], email=row['email'])
            u.set_password(row['password'])
        context.users[u.username] = u
        u.save()

@given(u'memiliki beberapa  data project')
def impl(context):
    from pumpkin.models import Project
    context.projects = {}
    for row in context.table:
        p = Project(name=row['name'],
                    identifier=row['identifier'])
        p.save()
        p.managers.add(context.users.get(row['manager']))
        context.projects[row['identifier']] = p
    assert True

@given(u'telah login sebagai "{username}" menggunakan password "{password}"')
def impl(context, username, password):
    br = context.browser
    br.get(context.browser_url('/'))
    br.find_element_by_name('username').send_keys(username)
    br.find_element_by_name('password').send_keys(password)
    br.find_element_by_tag_name('form').submit()


@when(u'mengklik logo sistem')
def impl(context):
    context.browser.find_element_by_link_text('pumpkin').click()


@then(u'Saya akan melihat daftar project berikut')
def impl(context):
    assert True



