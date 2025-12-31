# Django API Social Auth Demo

This project demonstrates a production-ready implementation of **Social Authentication (Google & GitHub)** for a Django API, using `dj-rest-auth`, `django-allauth`, and `django-rest-framework`.

It solves common compatibility issues and implements the **Authorization Code Flow**, designed to work with modern Frontends (React, Vue, etc.).

## Key Features
*   **API-First**: Returns JWTs (JSON Web Tokens) instead of session cookies.
*   **Google & GitHub Support**: Pre-configured providers.
*   **Custom Compatibility Shim**: Includes a custom `OAuth2Client` to bridge version conflicts between `dj-rest-auth` and `allauth`.

## Quick Start

### 1. Install Dependencies
```bash
pip install django djangorestframework dj-rest-auth django-allauth djangorestframework-simplejwt requests
```

### 2. Configure Environment
Set up your social apps in `settings.py` (or use environment variables):
*   `SOCIALACCOUNT_PROVIDERS['google']['APP']`
*   `SOCIALACCOUNT_PROVIDERS['github']['APP']`

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Run Server
```bash
python manage.py runserver
```

## How to Test (Without a Frontend)

You can verify the login flow manually using `curl`:

1.  **Get an Auth Code**: Open the provider's authorization URL in your browser.
    *   **Google**: `https://accounts.google.com/o/oauth2/v2/auth?...`
    *   **GitHub**: `https://github.com/login/oauth/authorize?...`
    *   *Note: Ensure `redirect_uri` matches `http://localhost:3000/callback` (Google) or `http://localhost:3000/github-callback` (GitHub).*

2.  **Exchange Code**:
    Copy the `code` parameter from the redirect URL and send it to the API:

    ```bash
    # For Google
    curl -X POST http://127.0.0.1:8000/api/auth/social/google/ \
         -H "Content-Type: application/json" \
         -d '{"code": "YOUR_CODE_HERE"}'

    # For GitHub
    curl -X POST http://127.0.0.1:8000/api/auth/social/github/ \
         -H "Content-Type: application/json" \
         -d '{"code": "YOUR_CODE_HERE"}'
    ```

3.  **Success**: You will receive a JSON response containing `access` (JWT), `refresh`, and user details.

## Implementation Details
See `core/views.py` for the critical `CustomOAuth2Client` implementation that prevents `TypeError` crashes found in standard setups.
