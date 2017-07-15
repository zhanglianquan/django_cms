from django.conf.urls import include, url
urlpatterns = [
    url(r'^cms_app/', include("cms_app.urls")),
]
