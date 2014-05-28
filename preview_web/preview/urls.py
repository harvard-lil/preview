from django.contrib import admin
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('preview.views',

    # Common Pages
    url(r'^$', 'common.generate_preview', name='common_generate_preview'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
