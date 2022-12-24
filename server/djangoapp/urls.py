from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    path(route='', view=views.get_dealerships, name='index'),
    # path for about view
    path(route='about', view=views.about, name='about'),  
    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),

    # path for registration
    path('registration/', views.registration_request, name='registration'),
    # path for login
    path('login/', views.login_request, name='login'),
    # path for logout
    path('logout/', views.logout_request, name='logout'),

    

    

    #Create a Django get_dealer_details view to get reviews of a dealer
    # path for dealer reviews view

    path('reviews/<int:dealer_id>/<str:dealer_name>', views.get_review_by_dealer, name='reviews'),

    # path for add a review view

    path('addreview/<int:dealer_id>/<str:dealer_name>', views.add_review, name='addreview')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)