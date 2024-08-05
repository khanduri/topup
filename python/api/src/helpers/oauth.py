import json
from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session


class UserOAuthModel(object):

    def __init__(self, access_code, social_network, social_id, username, email, name, domain=None):
        self.access_code = access_code
        self.social_network = social_network
        self.social_id = social_id
        self.username = username
        self.email = email
        self.name = name
        self.domain = domain

    def __str__(self):
        return "{}_{}_{}_{}_{}".format(self.social_network,
                                       self.social_id,
                                       self.username,
                                       self.email,
                                       self.domain,
                                       self.name)


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def get_callback_url(self):
        return url_for('users_views.oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]

    def callback(self):
        access_code, raw_json = self._fetch_raw_json()
        return self.parse_oauth_model(access_code, raw_json)

    def _fetch_raw_json(self):
        raise NotImplementedError

    @staticmethod
    def parse_oauth_model(access_code, raw_json):
        raise NotImplementedError


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            base_url='https://www.googleapis.com/plus/v1/people/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='https://www.googleapis.com/auth/userinfo.email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def _fetch_raw_json(self):
        if 'code' not in request.args:
            return None, None

        code = request.args['code']
        oauth_session = self.service.get_auth_session(
            data={'code': code,
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=json.loads
        )

        me = oauth_session.get('me').json()
        return code, me

    @staticmethod
    def parse_oauth_model(access_code, me):
        domain = me.get('domain')
        # me_email = None
        # for e in me['emails']:
        #     if e['type'] == 'account':
        #         me_email = e['value']
        me_email = me.get('email')

        if not domain and me_email:
            domain = me_email.split('@')[1]

        social_id = me['id']
        username = me.get('name')

        return UserOAuthModel(access_code, 'google', social_id, username, me_email, username, domain=domain)


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def _fetch_raw_json(self):
        if 'code' not in request.args:
            return None, None

        access_code = request.args['code']
        data = {
            'code': access_code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.get_callback_url()
        }
        oauth_session = self.service.get_auth_session(data=data, decoder=json.loads)
        me = oauth_session.get('me').json()
        return access_code, me

    @staticmethod
    def parse_oauth_model(access_code, me):
        social_id = me['id']
        email = me.get('email', '')
        username = email.split('@')[0]  # Facebook does not provide username
        name = me.get('name')

        return UserOAuthModel(access_code, 'facebook', social_id, username, email, name)


class TwitterSignIn(OAuthSignIn):
    def __init__(self):
        super(TwitterSignIn, self).__init__('twitter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )

    def authorize(self):
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url()}
        )
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def _fetch_raw_json(self):
        request_token = session.pop('request_token')
        access_code = None  # TODO: Get the code here
        if 'oauth_verifier' not in request.args:
            return None, None

        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )
        me = oauth_session.get('account/verify_credentials.json').json()

        return access_code, me

    @staticmethod
    def parse_oauth_model(access_code, me):
        social_id = str(me.get('id'))
        username = me.get('screen_name')
        email = None  # Twitter does not provide email
        name = None

        return UserOAuthModel(access_code, 'twitter', social_id, username, email, name)
