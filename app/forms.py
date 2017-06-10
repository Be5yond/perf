# -*- coding: utf-8 -*-
from django import forms
from .models import Host, Profile, Task, Tool


TOOL_CHOICES = tuple((t, t.name) for t in Tool.objects.all())


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['name', 'ip', 'user', 'password']
        
        
class ProfForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'desc', 'tool', 'params']
    
    params = forms.CharField(widget=forms.Textarea)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'desc', 'host', 'tool', 'profile']

    tool = forms.CharField(max_length=255, label="测试工具",
                           widget=forms.Select(choices=TOOL_CHOICES))
