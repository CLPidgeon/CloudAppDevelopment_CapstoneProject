from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path(route='', view=views.get_dealerships, name='index'),
    # path for about view
    path(route="about/", view=views.about, name="about"),
    # path for contact us view
    path(route="contact/", view=views.contact, name="contact"),
    # path for registration
    path('registration/', views.registration_request, name='registration'),
    # path for login
    path('login/', views.login_request, name='login'),
    # path for logout
    path('logout/', views.logout_request, name='logout'),
    path('dealership/<str:dealer_id>/', views.get_dealerships_by_id, name='dealer_details'),
    # path for dealer reviews view
    path('dealership/<int:dealer_id>/review', views.get_dealership_review, name='dealer_reviews'),
    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
