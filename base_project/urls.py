from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testProj.views.home', name='home'),
    # url(r'^testProj/', include('testProj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    (r'^$', TemplateView.as_view(template_name='views/home.html'))
)

if settings.DEBUG:
    # Ensure we serve static and media files when running in debug mode
    # (probably they are not handled by a dedicated webserver)

    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    
