# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_auth.registration.views import SocialLoginView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


# Create your views here.
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'https://developers.google.com/oauthplayground'