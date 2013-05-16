# -*- coding: utf-8 -*-
from django import forms
from pumpkin import models

class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['name', 'identifier', 'description']
