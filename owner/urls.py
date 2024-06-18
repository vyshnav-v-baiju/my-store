from django.urls import path
from owner import views



urlpatterns=[

    path("register",views.SignUp.as_view()),
    path('home',views.HomeView.as_view()),
    path('signin',views.SignIn.as_view()),
    path('productadd',views.ProductAddView.as_view())
]