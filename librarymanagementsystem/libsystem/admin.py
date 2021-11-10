from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.



class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = SiteUser
        fields = ('email', )

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = SiteUser
        fields = ('name','email', 'password')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin():
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_filter = ( 'department',)  

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name',)}
         ),
    )
    search_fields = ('email', 'name')
    ordering = ('id',)
    filter_horizontal = ()




class expbook(ImportExportModelAdmin):
    list_display = ('title', 'author', 'summary','isbn', 'total_copies','available_copies','pic')
    list_filter = ( 'title',)

admin.site.register(Book,expbook)
admin.site.register(SiteUser)
admin.site.register(User)
admin.site.unregister(Group)