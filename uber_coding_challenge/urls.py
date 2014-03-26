from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from bike_parkings import views

urlpatterns = patterns('',
    url(r'^bike_parkings/', include('bike_parkings.urls', namespace="bike_parkings")),
    url(r'^admin/', include(admin.site.urls)),
)
