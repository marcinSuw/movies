from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()

class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'password',
            'date_joined',
        )

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserModelForm

    date_hierarchy = 'date_joined'
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )
    fields = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'password',
        'date_joined',
        'groups',
    )
    readonly_fields = ('date_joined',)
    filter_horizontal = ('groups',)

