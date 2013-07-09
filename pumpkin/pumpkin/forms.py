# -*- coding: utf-8 -*-
from django import forms
from pumpkin import models

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ('name', 'identifier', 'description')

class NewRepositoryForm(forms.ModelForm):
    class Meta:
        model = models.Repository
        fields = ('scm', 'address')


class NewServerForm(forms.ModelForm):
    class Meta:
        model = models.Server
        fields = ('host', 'port', 'superuser_password',
                  'user_login', 'user_password')
