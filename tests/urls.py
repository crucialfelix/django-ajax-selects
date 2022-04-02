from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

from ajax_select import urls as ajax_select_urls

admin.autodiscover()

urlpatterns = [
                  path('ajax_lookups/', include(ajax_select_urls)),
                  path('admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
