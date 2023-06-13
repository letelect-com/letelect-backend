from django.urls import path
from knox import views as knox_views
from . import views

app_name = 'api'

# overview of all urls
urlpatterns = [
    path('', views.TestAPI.as_view(), name='test'),
    path('test/', views.TestAPI.as_view(), name='test'),
]

# accounts urls
urlpatterns += [
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('signup-client/', views.SignUpClientAPI.as_view(), name='signup-client'),
    path('register-staff/', views.RegisterStaffAPI.as_view(), name='register-staff'),
    path('user-profile/', views.UserProfileAPI.as_view(), name='user_profile'),
    path('change-password/', views.ChangePasswordAPI.as_view(), name='change-password'),  # noqa
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
]

# voters urls
urlpatterns += [
    path('voters/', views.VotersListAPI.as_view(), name='voters'),
]


# elections urls
urlpatterns += [
    path('elections/', views.ElectionsListAPI.as_view(), name='elections'),
]

# contacts urls
urlpatterns += [
    path('contact-us/', views.ContactUsAPI.as_view(), name='contact_us'),
    path('contacts/', views.ContactUsListAPI.as_view(), name='contacts'),

]
