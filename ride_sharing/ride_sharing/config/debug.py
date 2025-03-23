from django.conf import settings

if settings.DEBUG:
    settings.INSTALLED_APPS += ["debug_toolbar"]
    settings.MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
