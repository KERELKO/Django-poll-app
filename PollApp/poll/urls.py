from django.urls import path
from . import views
from . import auth_views


app_name = 'poll'

urlpatterns = [
	path('', views.PollListView.as_view(), 
		 name='list'),
	path('create/', views.PollCreateView.as_view(), 
		 name='create'),
	path('edit/<pk>/', views.PollEditView.as_view(), 
		 name='edit'),
	path('detail/<pk>/', views.PollDetailView.as_view(), 
		 name='detail'),
	path('detail/<pk>/result/', views.PollResultView.as_view(),
		 name='result'),
	path('delete/<pk>/', views.PollDeleteView.as_view(),
		 name='delete'),
	# auth
	path('login/', auth_views.UserLoginView.as_view(),
		 name='login'),
	path('logout/', auth_views.UserLogout.as_view(),
      	 name='logout'),
	path('registration/', auth_views.UserRegistrationView.as_view(),
		 name='registration'),
]
