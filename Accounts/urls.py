from django.urls import path, include

from .views import (UserCreate,
                    PasswordChangeView,
                    CreateTokenView,
                    GoogleLogin,
                    RenterView,
                    RenterPrefView,
                    RenterPrefLocationView,
                    AgentView,
                    AgencyView,
                    OwnerView, emailAvailablity,TestAuth)

viewMethods = {'get': 'retrieve', 'put': 'update', 'post': 'create'}
userCreateViewMethods = {'get': 'retrieve',
                         'put': 'update',
                         'post': 'create',
                         'delete': 'destroy'}
urlpatterns = [
    # Account Related Path
    path('accounts/', UserCreate.as_view(userCreateViewMethods), name='account-create'),
    path('accounts/change-password', PasswordChangeView.as_view({'post': 'update_password'}),
         name='account-password-change'),
    path('token/', CreateTokenView.as_view(), name='account-create'),
    path('accounts-auth/', include('allauth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    # Renter Related Paths
    path('renter/', RenterView.as_view(viewMethods), name='renter-create'),
    path('renter-pref/', RenterPrefView.as_view(viewMethods),
         name='renter-pref-view'),
    path('renter-pref-loc/', RenterPrefLocationView.as_view(viewMethods),
         name='renter-pref-loc-view'),
    # Agent Related Path
    path('agent/', AgentView.as_view(viewMethods),
         name='agent-view'),
    path('agency/', AgencyView.as_view(viewMethods),
         name='agency-view'),
    # Owner Related Path
    path('owner/', OwnerView.as_view(viewMethods),
         name='owner-view'),
    path('checkEmail/',emailAvailablity, name='email-available'),
    path('test/',TestAuth.as_view(), name='test'),

]
