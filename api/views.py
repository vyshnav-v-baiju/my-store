from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.views import Response

from rest_framework.viewsets import ViewSet,ModelViewSet
from django.contrib.auth.models import User



from api.models import product,Carts,Reviews
from api.serializer import ProductSerializer,ProductModelSerializer,UserSerializer,CartSerializer,ReviewSerializer
from rest_framework.decorators import action
from rest_framework import authentication,permissions


class productView(APIView):
    def get(self,request,*args,**kw):

        qs = product.objects.all()

        serializer = ProductSerializer(qs,many=True)
        
        return Response(data =serializer.data)
    
    def post(self,request,*args,**aws):

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            print(serializer.validated_data)

            product.objects.create(**serializer.validated_data)

            return Response(data =serializer.data)
        else:
            return Response(serializer.errors)
    
class ProductSingleView(APIView):
    
    def get(self,request,*args,**kw):
        id = kw.get("id")
        qs = product.objects.get(id=id)

        serializer = ProductSerializer(qs,many=False)

        return Response(data = serializer.data)
    
    def put(self,request,*args,**kw):

        serializer = ProductSerializer(data=request.data)
        id = kw.get("id")
        if serializer.is_valid():
            product.objects.filter(id = id).update(**request.data)
            return Response(data = serializer.data)
        else:
            return Response(data = serializer.errors)

    def delete(self,request,*args,**kw):

        id = kw.get("id")
        product.objects.filter(id = id).delete()

        return Response(data = 'delete of a product')




# class viewproduct(ViewSet):
    
#     def list(self,request,*args,**kw):

#         qs = product.objects.all()

#         serializer = ProductSerializer(qs,many=True)
        
#         return Response(data =serializer.data)
    

#     def create(self,request,*args,**kw):
#         serializer = ProductModelSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(data = request.data)
#         else:
#             return Response(data = serializer.errors)


#     def retrieve(self,request,*args,**kw):

#         id = kw.get("pk")
#         qs = product.objects.get(id=id)

#         serializer = ProductModelSerializer(qs,many=False)

#         return Response(data = serializer.data)
    

#     def update(self,request,*args,**kw):
        
#         id = kw.get("pk")
#         obj = product.objects.get(id = id)
#         serializer = ProductModelSerializer(data=request.data,instance=obj)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data = serializer.data)
#         else:
#             return Response(data = serializer.errors)


#     def destroy(self,request,*args,**kw):
#         id = kw.get("pk")
#         product.objects.filter(id = id).delete()

#         return Response(data = 'delete of a product')
    
#     @action(methods=['GET'],detail=False)
#     def categories(self,request,*args,**kw):
#         result = product.objects.values_list("catagory",flat=True).distinct()

#         return Response(data= result)
    
#     @action(methods=['GET'],detail=False)
#     def descriptions(self,request,*args,**kw):
#         result = product.objects.values_list("description",flat=True).distinct()

#         return Response(data= result)
    

# class UserView(ViewSet):
#     def create(self,request,*args,**kw):
#         serialzer = UserSerializer(data=request.data)

#         if serialzer.is_valid():
#             serialzer.save()
#             return Response(data=serialzer.data)
#         else:
#             return Response(data=serialzer.errors)
        
class ProductModelViewset(ModelViewSet):

    serializer_class = ProductModelSerializer
    queryset = product.objects.all()
    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["POST"],detail=True)
    def addto_cart(self,request,*args,**kw):

        id = kw.get("pk")
        item = product.objects.get(id=id)
        user = request.user
        user.carts_set.create(products=item)

        return Response(data='item added to cart')
    @action(methods=['POST'],detail=True)
    def add_review(self,request,*args,**kw):
        
        user = request.user
        id =kw.get('pk')
        object = product.objects.get(id=id)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(products= object,user = user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=['GET'],detail=True)  
    def reviwes(self,request,*args,**kw):
        id = kw.get("pk")
        product =product.objects.get(id=id)

        qs= product.reviews_set.all()
        serializer = ReviewSerializer(qs,many=True)
        return Response(data=serializer.data)


class UserViewset(ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

class CartView(ModelViewSet):

    serializer_class = CartSerializer
    queryset = Carts.objects.all()

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # def post(self,request,*args,**kw):

        # id = kw.get("id")
        # item = product.objects.get(id=id)
        # user = request.user
        # user.carts_set.create(products=item)

        # return Response(data='item added to cart')

    def list(self, request,args,*kw):
        
        qs = request.user.carts_set.all()
        serializer = CartSerializer(qs,many=True)
        return Response(data=serializer.data)
   

class ReviewDeleteview(APIView):
    def delete(self,request,*args,**kw):
        id = kw.get('pk')

        Reviews.objects.filter(id=id).delete
        return Response(data='review deleted')
        