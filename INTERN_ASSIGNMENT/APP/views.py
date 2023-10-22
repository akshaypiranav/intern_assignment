"""
INTERN - AKSHAY PIRANAV B
G-MAIL - akshaypiranavb@gmail.com
"""

from django.http import  JsonResponse
from django.shortcuts import redirect, render
from APP.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
 
#HOEM PAGE
def home(request):
  products=Product.objects.filter(trending=1) #GETTING THE TRENDING PRODUCTS WHICH ARE HAVING TRENDING=1(TRUE)
  return render(request,"shop/index.html",{"products":products})

#FAVOURITE PAGE
def favviewpage(request):
  if request.user.is_authenticated: #ENSURE THAT USER IS AUTHENTICATED BECAUSE THE VALUES STORED IN THE FAVPAGE IS BASED ON THE USER
    fav=Favourite.objects.filter(user=request.user) #CHECKS THE USER IN THE FAVOURITE TABLE WITH THE CURRENT USER
    return render(request,"shop/fav.html",{"fav":fav})#SENDS THE VALUES ALONG WITH THE RENDER
  else:
    return redirect("/") #IF NOT AUTHENTICATED THEN REDIRECTS TO THE HOME PAGE
 
#REMOVING FAVOURITE ITEM
def remove_fav(request,fid):#GETS THE ID OF THE FAV PRODUCT
  item=Favourite.objects.get(id=fid)#GETS THE ITEM
  item.delete() #FINALLY DELETES THE PRODUCT WHICH IS STORED IN THE FAVORITE TABLE
  return redirect("/favviewpage")
 
 
 
#CART PAGE
def cart_page(request):
  if request.user.is_authenticated:#ENSURE THAT USER IS AUTHENTICATED BECAUSE THE VALUES STORED IN THE CART IS BASED ON THE USER
    cart=Cart.objects.filter(user=request.user)#CHECKS THE USER IN THE CART TABLE WITH THE CURRENT USER
    return render(request,"shop/cart.html",{"cart":cart})#SENDS THE VALUES ALONG WITH THE RENDER
  else:
    return redirect("/")#OTHERWISE REDIRECTED TO HOMEPAGE
 

#REMOVING ITEM FROM THE CART
def remove_cart(request,cid):#GETS THE ID OF THE CART PRODUCT
  cartitem=Cart.objects.get(id=cid)#GETS THE ITEM
  cartitem.delete()#FINALLY DELETES THE PRODUCT STORED IN THE CART
  return redirect("/cart")#REDIRECTED TO THE SAME PAGE
 
 


def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest': #ASYNCHRONOUS REQUEST TO THE SERVER
    if request.user.is_authenticated: #CHECKS WHEATHER USER IS LOGGED IN BECAUSE THE PROCESS ON USER
      data=json.load(request) #JSON DATA
      product_id=data['pid']#EXTRACT THE PID SEND FROM THE JAVASCRIPT(CLIENT)
      product_status=Product.objects.get(id=product_id)#GETS THE PRODUCT ACCORDING TO THAT ID
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id): #CHECKS THE TABLE FAVOURITE WHEATHER IT ALREADY HAVE THE DATA IN IT
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)#IF YES RETURN THESE
         else:
          Favourite.objects.create(user=request.user,product_id=product_id) #IF NOT IT ADDS TO THE TABLE FAVOURITE
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)#THEN SHOWS THE ACKNOWLEDGEMENT
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)#IF NOT LOGGED IN THEN SHOWS THESE
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)#IF NOT A XMLHttpRequest shows these
 
 
def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':#ASYNCHRONOUS REQUEST TO THE SERVER
    if request.user.is_authenticated:#CHECKS WHEATHER USER IS LOGGED IN BECAUSE THE PROCESS ON USER
      data=json.load(request) #JSON DATA
      product_qty=data['product_qty']#EXTRACT THE QUANTITY SEND FROM THE JAVASCRIPT(CLIENT)
      product_id=data['pid']#EXTRACT THE PID SEND FROM THE JAVASCRIPT(CLIENT)
      #print(request.user.id)
      product_status=Product.objects.get(id=product_id)#GET THE DATA ACCORIDING TO THE REQUEST
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id): #IF ALREADY HAVE THE DATA
          return JsonResponse({'status':'Product Already in Cart'}, status=200) #THEN SHOWS THIS
        else:
          if product_status.quantity>=product_qty:#CHECKS THE QUANTITY
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)#CREATES THE VALUE TO THE USER IN THE CART TABLE
            return JsonResponse({'status':'Product Added to Cart'}, status=200)#SHOWS THESE
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200) #IF NOT QUANTITY AVAILABLE THEN THESE
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200) #IF NOT LOGGED IN
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)# IF NOT THAT XMLHttpRequest then these shown

#LOGOUT
def logout_page(request):
  if request.user.is_authenticated:#CHECKS THE AUTHENTICATION AND LOGOUT THE USER
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")
 
#LOGIN PAGE
def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':#GETS THE VALUE IN THE POST METHOD
      name=request.POST.get('username')#GETTING THE VALUES
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)#CHECKS THE USER MATCHES THE USERS IN THE DATABASE
      if user is not None:
        login(request,user)#THEN LOGIN
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")#OTHERWISE REDIRECTS TO THE LOGIN PAGE
    return render(request,"shop/login.html")

#REGISTRATION PAGE
def register(request):
  form=CustomUserForm()
  if request.method=='POST':#IF POST METHOD
    form=CustomUserForm(request.POST) #CHECKS THE VALUES WHICH ARE TYPED IN THE FORM
    if form.is_valid(): #IF VALID
      form.save()#THEN SAVE THE VALUES IN THE DB
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"shop/register.html",{'form':form})
 
#COLLECTION PAGE
def collections(request):
  #SHOWS THE NON HIDDEN CATEGORY LIKE BOOKS IN THE COLLECTION PAGE
  catagory=Catagory.objects.filter(status=0)
  return render(request,"shop/collections.html",{"catagory":catagory})
 
#COLLECTION SPECIFIC
def collectionsview(request,name):
  if(Catagory.objects.filter(name=name,status=0)):#NON HIDDEN CATEGORY
      products=Product.objects.filter(category__name=name)#THE SELECTED AND RETURN THE VALUES WHICH ARE COMES UNDER THE THAT SPECIFIC CATEGORY
      return render(request,"shop/products/index.html",{"products":products,"category_name":name})
  else:
    #IF NOT NO SUCH CATEGORY
    messages.warning(request,"No Such Catagory Found")
    return redirect('collections')
 
#SPECIFIC PRODUCT
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):#CHECKS WHEATHER THE CATEGORY AVAILABLE IN CATAGORY  TABLE
      if(Product.objects.filter(name=pname,status=0)):#CHECKS WHEATHER THE PRODUCT AVAILABLE IN THE PRODUCT TABLE
        products=Product.objects.filter(name=pname,status=0).first()#FETCHES THAT SPECIFIC PRODUCT AND RETURN
        return render(request,"shop/products/product_details.html",{"products":products})
      else:
        #IF NO PRODUCT
        messages.error(request,"No Such Produtct Found")
        return redirect('collections')
    else:
      # IF NO CATEGORY
      messages.error(request,"No Such Catagory Found")
      return redirect('collections')