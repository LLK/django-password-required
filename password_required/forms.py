# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class AuthenticationForm(forms.Form):
    """
    Simple form to allow users to access a page via a password.

    A copy of django.contrib.auth.forms.AuthenticationForm, adapted to this
    much simpler use case.
    """
    password = forms.CharField(label=_("Access Code"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        super(AuthenticationForm, self).__init__(*args, **kwargs)


    def clean_password(self):
        """
        Validate that the password entered was correct.
        """
        password = self.cleaned_data.get('password')
        valid_passwords = getattr(settings, 'PASSWORD_REQUIRED_PASSWORD', None)
        
        if not valid_passwords:
            raise forms.ValidationError(_("PASSWORD_REQUIRED_PASSWORD is not set, and thus it is currently impossible to log in."))

        fail = True
        for pswd in valid_passwords:
            if (password == pswd or password.strip() == pswd):
                fail = False
      
        if fail:
            raise forms.ValidationError(_("Invalid code. If you've accessed the site before, just enter the password you used previously."))


        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data

