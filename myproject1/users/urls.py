from django.urls import path
from .views import SignupView, LoginView,UserSearchView,SendFriendRequestView,AcceptFriendRequestView,RejectFriendRequestView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('accept/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('reject/<int:pk>/', RejectFriendRequestView.as_view(), name='reject-friend-request'),

]