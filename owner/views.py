from django.shortcuts import render
from django.views.generic import View
from owner.forms import LoginForm,RegistrationForm,ProductForm


# Create your views here.



class HomeView(View):
    def get(self,request,*args,**kw):
        return render(request,'Home.html')
    
class SignUp(View):
    def get(self,request,*args,**kw):
        form =RegistrationForm()
        return render(request,'register.html',{"form":form})
    
class SignIn(View):
    def get(self,request,*args,**kw):

        form =LoginForm()
        return render(request,'login.html',{"form":form})
    
    
    def post (self,request,*args,**kw):

        print(request.POST)
        print(request.POST.get("usename"))
        print(request.POST.get("Password"))

        return render(request,'Home.html')
    
class ProductAddView(View):

    def get(self,request,*args,**kw):
        form = ProductForm()

        return render(request,"product_add.html",{"form":form})
    
    def post(self,request,*args,**kw):
        
        form=ProductForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return render(request,"home.html")
        else:
            return render(request,"product_add.html",{"form":form})

        
    
    

    
