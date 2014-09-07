from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from co2.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'calculadora.views.home', name='home'),
    # url(r'^calculadora/', include('calculadora.foo.urls')),
    url(r'^$', 'co2.views.entidades', name='main'),
    url(r'^test/', 'co2.views.test',name='test'),    
    (r'^grappelli/', include('grappelli.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),    
    # accounts
    url(r'^user/profile/', 'co2.views.userprofile'), 
    url(r'^mi-cuenta/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'},name='auth_logout'),
    url(r'^mi-cuenta/login/$', 'django.contrib.auth.views.login', name='auth_login'),    
    url(r'^mi-cuenta/', include('registration.backends.default.urls')),    
    url(r'^anual/$', 'co2.views.anual', name="anual"),  
    url(r'^(?P<entidad>\w+)/consumos/$', login_required(AddConsumoView.as_view()), name="AddConsumoView"),
    url(r'^informes/(?P<entidad>\w+)/(?P<ano>\d+)/$', 'co2.views.informe_local', name="informe_local"),
    url(r'^informes2/(?P<entidad>\w+)/(?P<ano>\d+)/$', 'co2.views.informe_anual', name="informe_anual"),          
    url(r'^(?P<entidad>\w+)/$', 'co2.views.main', name="main"),
    url(r'^(?P<entidad>\w+)/(?P<ano>\d+)/$', 'co2.views.main', name="main_anual"),
    url(r'^(?P<entidad>\w+)/(?P<ano>\d+)/csv/$', 'co2.views.export_csv_pivot', name="csv2"), 
    url(r'^csv/', 'co2.views.export_csv_pivot', name="csv"),   
    url(r'^(?P<entidad>\w+)/historico/$', 'co2.views.historico', name="historico"),
    url(r'^(?P<entidad>\w+)/info/locales/$', 'co2.views.info_locales', name="info"),
    url(r'^(?P<entidad>\w+)/info/locales/(?P<id>\w+)$', 'co2.views.detalle_local', name="detalle_local"),
    url(r'^(?P<entidad>\w+)/info/locales/(?P<id>\w+)/(?P<ano>\d+)/$', 'co2.views.detalle_local', name="detalle_local_ano"),
    url(r'^(?P<entidad>\w+)/info/vehiculos/$', 'co2.views.info_vehiculos', name="info"),    
    url(r'^(?P<entidad>\w+)/info/vehiculos/(?P<id>\w+)$', 'co2.views.detalle_vehiculo', name="detalle_vehiculo"),
    url(r'^(?P<entidad>\w+)/info/vehiculos/(?P<id>\w+)/(?P<ano>\d+)/$', 'co2.views.detalle_vehiculo', name="detalle_vehiculo_ano"),   
    url(r'^(?P<entidad>\w+)/acumulado/(?P<ano>\d+)/$', 'co2.views.acumulado', name="acumulado"),
    url(r'^(?P<entidad>\w+)/(?P<ano>\d+)/locales$', 'co2.views.locales', name="locales"),
    url(r'^(?P<entidad>\w+)/(?P<ano>\d+)/acumulado$', 'co2.views.acumulado', name="acumulado"),
    url(r'^(?P<entidad>\w+)/(?P<ano>\d+)/compare$', 'co2.views.compare', name="compare"),     
    url(r'^accounts/', include('registration.backends.default.urls')),     
    url(r' accounts/',include('registration')),
    

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

