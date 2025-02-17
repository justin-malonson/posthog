"""
Django settings for PostHog Enterprise Edition.
"""
import os
from typing import Dict, List

from posthog.settings import AUTHENTICATION_BACKENDS, DEMO, SITE_URL, DEBUG
from posthog.settings.utils import get_from_env
from posthog.utils import str_to_bool

# Zapier REST hooks
HOOK_EVENTS: Dict[str, str] = {
    # "event_name": "App.Model.Action" (created/updated/deleted)
    "action_performed": "posthog.Action.performed",
}

# SSO
AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + [
    "ee.api.authentication.MultitenantSAMLAuth",
    "social_core.backends.google.GoogleOAuth2",
]

# SAML base attributes
SOCIAL_AUTH_SAML_SP_ENTITY_ID = SITE_URL
SOCIAL_AUTH_SAML_SECURITY_CONFIG = {
    "wantAttributeStatement": False,  # AttributeStatement is optional in the specification
    "requestedAuthnContext": False,  # do not explicitly request a password login, also allow multifactor and others
}
# Attributes below are required for the SAML integration from social_core to work properly
SOCIAL_AUTH_SAML_SP_PUBLIC_CERT = ""
SOCIAL_AUTH_SAML_SP_PRIVATE_KEY = ""
SOCIAL_AUTH_SAML_ORG_INFO = {"en-US": {"name": "posthog", "displayname": "PostHog", "url": "https://posthog.com"}}
SOCIAL_AUTH_SAML_TECHNICAL_CONTACT = {"givenName": "PostHog Support", "emailAddress": "hey@posthog.com"}
SOCIAL_AUTH_SAML_SUPPORT_CONTACT = SOCIAL_AUTH_SAML_TECHNICAL_CONTACT


# Google SSO
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
if "SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS" in os.environ:
    SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS: List[str] = os.environ[
        "SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS"
    ].split(",")
elif DEMO:
    # Only PostHog team members can use social auth in the demo environment
    # This is because in the demo env social signups get is_staff=True to facilitate instance management
    SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ["posthog.com"]

# Schedule to run column materialization on. Follows crontab syntax.
# Use empty string to prevent from materializing
MATERIALIZE_COLUMNS_SCHEDULE_CRON = get_from_env("MATERIALIZE_COLUMNS_SCHEDULE_CRON", "0 5 * * SAT")
# Minimum query time before a query if considered for optimization by adding materialized columns
MATERIALIZE_COLUMNS_MINIMUM_QUERY_TIME = get_from_env("MATERIALIZE_COLUMNS_MINIMUM_QUERY_TIME", 3000, type_cast=int)
# How many hours backwards to look for queries to optimize
MATERIALIZE_COLUMNS_ANALYSIS_PERIOD_HOURS = get_from_env(
    "MATERIALIZE_COLUMNS_ANALYSIS_PERIOD_HOURS", 7 * 24, type_cast=int
)
# How big of a timeframe to backfill when materializing event properties. 0 for no backfilling
MATERIALIZE_COLUMNS_BACKFILL_PERIOD_DAYS = get_from_env("MATERIALIZE_COLUMNS_BACKFILL_PERIOD_DAYS", 90, type_cast=int)
# Maximum number of columns to materialize at once. Avoids running into resource bottlenecks (storage + ingest + backfilling).
MATERIALIZE_COLUMNS_MAX_AT_ONCE = get_from_env("MATERIALIZE_COLUMNS_MAX_AT_ONCE", 10, type_cast=int)

BILLING_SERVICE_URL = get_from_env("BILLING_SERVICE_URL", "https://billing.posthog.com")

# Whether to enable the admin portal. Default false for self-hosted as if not setup properly can pose security issues.
ADMIN_PORTAL_ENABLED = get_from_env("ADMIN_PORTAL_ENABLED", DEMO or DEBUG, type_cast=str_to_bool)

ASSET_GENERATION_MAX_TIMEOUT_MINUTES = get_from_env("ASSET_GENERATION_MAX_TIMEOUT_MINUTES", 10, type_cast=int)
