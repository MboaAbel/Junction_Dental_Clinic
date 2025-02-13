"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from django.conf import settings



urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),
    path('', include('Clinic.urls')),
    path('Accounts/', include('Accounts.urls')),
    path('accounts/', include('Accounts.urls')),
    path('Dashboard/', include('Dashboard.urls')),
    path('Doctors/', include('doctors.urls')),
    path('Mpesa/', include('mpesa.urls')),
    path('Reception/', include('bookings.urls')),
    path('Patients/', include('Appointment.urls')),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
