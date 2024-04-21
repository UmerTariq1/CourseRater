from django.urls import path
from . import views
from .views import course_list, course_detail
from .views import register_request, login_request, logout_request


urlpatterns = [
    path('', views.course_list, name='course_list'),
    # for course_detail view : an id is required
    path('course/<int:course_id>/', course_detail.as_view(), name='course_detail'),
    path('submit_rating', views.course_list, name='submit_rating'),

    path('login/', login_request, name='login'),
    path('register/', register_request, name='register'),
    path('logout/', logout_request, name='logout'),
    
    # path('add/', views.add_menu_item, name='add_menu_item'),
    # path('login/', views.login_view, name='login'),
    # path('signup/', views.signup_view, name='signup'),
]
