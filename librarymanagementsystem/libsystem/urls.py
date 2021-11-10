from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .views import *

app_name = 'siteuser'

urlpatterns = [
    path('',index,name="index"),      
    path('logout',Signout, name="logout"),
    path('signup',SignupView.as_view(), name="signup"),   
    path('login', LoginView.as_view(), name="login"),
    path('books',BooksView.as_view(), name="books"),
    path('add-books',AddBookView.as_view(), name="add-books"),
    path('update-book/<int:book_id>',UpdateBookView.as_view(), name="update-book"),
    path('delete-book/<int:book_id>',DeleteBookView.as_view(), name="delete-book"),

    path('profile', ProfileView.as_view(), name="profile"),
    path('updateprofile', UpdateProfileView.as_view(), name="updateprofile"),
    path('changepassword', ChangePasswordView.as_view(), name="changepassword"),
    path('users', UsersView.as_view(), name="users"),
    path('update-user/<int:user_id>', UpdateUserView.as_view(), name="update-user"),
    path('delete-user/<int:user_id>',DeleteUserView.as_view(), name="delete-user"),
    path('upload-csv/', profile_upload, name="profile_upload"),
]