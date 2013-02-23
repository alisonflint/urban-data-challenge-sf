from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^ajax/', include('ajax.urls')),
    (r'', 'bus_distance.views.index'),
    # Examples:
    # url(r'^$', 'urban_time.views.home', name='home'),
    # url(r'^urban_time/', include('urban_time.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
