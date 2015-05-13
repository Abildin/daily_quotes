from django.conf.urls import include, url, patterns
from django.contrib import admin
from tastypie.api import Api
from quotes import views
from quotes.api import QuoteResource

v1_api = Api(api_name='v1')
v1_api.register(QuoteResource())

urlpatterns = patterns(
	'',
    url(r'^$', views.manager, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)