from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('restApiCP.urls')),
]

if settings.DEBUG:
  urlpatterns += static(settings.UPLOAD_URL, document_root=settings.UPLOAD_ROOT)

