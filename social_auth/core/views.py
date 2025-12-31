from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client



class CustomOAuth2Client(OAuth2Client):
    def __init__(
        self,
        request,
        consumer_key,
        consumer_secret,
        access_token_method,
        access_token_url,
        callback_url,
        scope,
        scope_delimiter=" ",
        headers=None,
        basic_auth=False,
    ):
        super().__init__(
            request=request,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_method=access_token_method,
            access_token_url=access_token_url,
            callback_url=callback_url,
            scope_delimiter=scope_delimiter,
            headers=headers,
            basic_auth=basic_auth,
        )


class DebuggingGitHubAdapter(GitHubOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        try:
            print(f"DEBUG: Attempting to complete login with token: {token}")
            return super().complete_login(request, app, token, **kwargs)
        except Exception as e:
            print("--- GITHUB LOGIN ERROR ---")
            import traceback
            traceback.print_exc()
            if hasattr(e, 'response'):
                print("GitHub Response Status:", e.response.status_code)
                print("GitHub Response Body:", e.response.text)
            print("--------------------------")
            raise e


class GitHubLogin(SocialLoginView):
    adapter_class = DebuggingGitHubAdapter
    callback_url = "http://localhost:3000/github-callback"
    client_class = CustomOAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/callback"
    client_class = CustomOAuth2Client
