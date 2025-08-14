import logging, os, json
from datetime import timedelta

# Basic
APP_NAME = os.getenv("engmx", "Superset")
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "nfidaofndasfdusbfoasnfaofnasofasfadadgfvvsgb")
SQLALCHEMY_DATABASE_URI = os.getenv(
    "SQLALCHEMY_DATABASE_URI", "sqlite:////app/superset_home/superset.db"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Cache (Redis)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": 1,
}

# Celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", f"redis://{REDIS_HOST}:{REDIS_PORT}/1")
RESULTS_BACKEND = CACHE_CONFIG  # optional, Superset uses own results backend too

# Security & sessions
ENABLE_PROXY_FIX = os.getenv("ENABLE_PROXY_FIX", "true").lower() == "true"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
# SESSION_COOKIE_SECURE= False
SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# CORS (if embedding/external UI)
_CORS = [x.strip() for x in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if x.strip()]
if _CORS:
    ENABLE_CORS = True
    CORS_OPTIONS = {"supports_credentials": True, "origins": _CORS}

# Feature flags
def _parse_ff(s):
    ff = {}
    for pair in (p.strip() for p in s.split(",") if p.strip()):
        k, _, v = pair.partition(":")
        ff[k.strip()] = v.strip().lower() in ("1", "true", "yes", "on")
    return ff

FEATURE_FLAGS = _parse_ff(os.getenv("FEATURE_FLAGS", ""))

# Limits & timeouts
ROW_LIMIT = int(os.getenv("ROW_LIMIT", "50000"))
SQLLAB_TIMEOUT = int(os.getenv("SQLLAB_TIMEOUT", "300"))

# Logging
LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOG_LEVEL = "INFO"

# Files live here (mounted volume)
DATA_DIR = "/app/superset_home"
UPLOAD_FOLDER = f"{DATA_DIR}/uploads/"
IMG_UPLOAD_FOLDER = f"{DATA_DIR}/uploads/"
CACHE_DEFAULT_TIMEOUT = 300

# Example: OIDC/LDAP placeholders (uncomment and configure for org)
# AUTH_TYPE = AUTH_OID
# OIDC_CLIENT_ID = os.getenv("OIDC_CLIENT_ID")
# OIDC_CLIENT_SECRET = os.getenv("OIDC_CLIENT_SECRET")
# OIDC_METADATA_URL = os.getenv("OIDC_METADATA_URL")

# Talisman security headers (enable behind TLS)
# TALISMAN_ENABLED = os.getenv("TALISMAN_ENABLED", "false").lower() == "true"

# TALISMAN_ENABLED = True
# TALISMAN_CONFIG = {
#     "content_security_policy": {
#         "default-src": ["'self'"],
#         "img-src": ["'self'", "data:"],
#         "style-src": ["'self'", "'unsafe-inline'"],
#         "script-src": ["'self'"],
#         # Add domains if embedding/iframes: "frame-ancestors": ["'self'", "https://your-app.example.com"],
#     }
# }
# # Optional: hide warning explicitly
# CONTENT_SECURITY_POLICY_WARNING = False