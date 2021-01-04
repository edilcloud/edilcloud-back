# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from web.views import FacebookLogin, GoogleLogin

urlpatterns = [
    # API DOCUMENTATION
    #url(r'^docs/', include('rest_framework_docs.urls')),

    # ADMIN URL
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls'), name='socialaccount_signup'),
    # DRF API URL
    #url(r'^api/backend/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/socials/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('api/auth/socials/google/', GoogleLogin.as_view(), name='google_login'),
    url('rest-auth/', include('social_django.urls', namespace='social')),
    # API FOR REGISTRATION, PASSWORD CHANGE, RESET, LOGIN etc
    url(r'^api/frontend/user/', include('apps.user.api.frontend.urls')),

    # JWT Social AUTH
    url(r'^api/login/', include('rest_social_auth.urls_jwt')),
    url(r'^api/frontend/payments/', include('apps.payments.api.frontend.urls')),

    url(r'^api/frontend/document/', include('apps.document.api.frontend.urls')),
    url(r'^api/frontend/media/', include('apps.media.api.frontend.urls')),
    url(r'^api/frontend/menu/', include('apps.menu.api.frontend.urls')),
    url(r'^api/frontend/message/', include('apps.message.api.frontend.urls')),
    url(r'^api/frontend/notify/', include('apps.notify.api.frontend.urls')),
    url(r'^api/frontend/product/', include('apps.product.api.frontend.urls')),
    url(r'^api/frontend/profile/', include('apps.profile.api.frontend.urls', namespace="api_frontend_profile")),
    url(r'^api/frontend/project/', include('apps.project.api.frontend.urls')),
    url(r'^api/frontend/quotation/', include('apps.quotation.api.frontend.urls')),
    url(r'^api/frontend/dashboard/', include('apps.dashboard.api.frontend.urls')),
    url('ws/', include('apps.ws.urls')),
]

if settings.DEBUG:
    # ON DEBUG

    # MEDIA
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # STATIC
    urlpatterns += staticfiles_urlpatterns()

    # DEBUG TOOLBAR
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
