from django.conf.urls import patterns, include, url
from django.contrib import admin
from webpage.views import redundancy

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', 'webpage.views.mainPage'),
    url(r'^hash/', 'webpage.views.hashGenerator'),
    url(r'^problemReg/', 'webpage.views.problemRegister'),
    url(r'^check/', 'webpage.views.checker'),
    url(r'^processingPage/', 'webpage.views.processingPage'),
    url(r'^contact/', 'webpage.views.contactPage'),
    url(r'^checkHash/', 'webpage.views.hashChecker'),
    url(r'^receivePiece/', 'webpage.views.pieceSender'),
    url(r'^sendPiece/', 'webpage.views.pieceReceiver'),
)

redundancy();