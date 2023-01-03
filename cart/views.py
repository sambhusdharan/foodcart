from django.shortcuts import render,redirect,get_object_or_404
from shop.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts import views
# Create your views here.



def c_id(request):
   id=request.session.session_key
   if not id:
       id=request.session.create()
   return id
@login_required(login_url='/accounts/login/')
def Cart_detail(request,tot=0,count=0,ct_item=None):
    if request.user.is_authenticated:
        try:
            ct = cartlist.objects.get(user=request.user)
            print(ct)
            ct_item = items.objects.filter(cart=ct)
            print( "cart_item",ct_item)
            for i in ct_item:
                tot += (i.prodt.price * i.quan)
                count += i.quan

        except ObjectDoesNotExist:
            pass
        print("count", count)
        return render(request, 'cart.html', {'ci': ct_item, 't': tot, 'cn': count})
    else:
        return redirect('login')
@login_required(login_url='login')
def addcart(request,product_id):
    if request.user.is_authenticated:
        prod = products.objects.get(id=product_id)
        try:
            print("1.-----------------------------------------------------------")
            # ct = cartlist.objects.get(user=request.user,cart_id=c_id(request))
            ct = cartlist.objects.get(user=request.user)
        except cartlist.DoesNotExist:
            print("2.-----------------------------------------------------------")
            ct = cartlist.objects.create(user=request.user,cart_id=c_id(request))
            ct.save()
        try:
            c_items = items.objects.get(prodt=prod, cart=ct)
            if c_items.quan < c_items.prodt.stock:
                c_items.quan += 1
            c_items.save()

        except items.DoesNotExist:
            c_items = items.objects.create(prodt=prod, quan=1, cart=ct)
            c_items.save()

        return redirect('CartDetails')
    else:
        return redirect('login')
@login_required(login_url='login')
def min_cart(request,product_id):
    if request.user.is_authenticated:
       cart_id = cartlist.objects.get(user=request.user)
       # cart_id = cartlist.objects.get(user=request.user, cart_id=c_id(request))
       prod = get_object_or_404(products,id=product_id)
       c_item=items.objects.get(prodt=prod,cart=cart_id)
       if c_item.quan > 1:
          c_item.quan -= 1
          c_item.save()
       else:
        c_item.delete()
       return redirect('CartDetails')
    else:
        return redirect('login')
@login_required(login_url='login')
def cart_delete(request,product_id):
     prod=get_object_or_404(products,id=product_id)
     cart_id = cartlist.objects.get(user=request.user)
     c_item = items.objects.get(prodt=prod, cart=cart_id)
     c_item.delete()
     # return render(request,'cart.html')

     return redirect('CartDetails')
@login_required(login_url='login')# error in this code
def payment(request,tot=0):
        ct = cartlist.objects.get(user=request.user)
        ct_item = items.objects.filter(cart=ct)
        for i in ct_item:
            tot += (i.prodt.price * i.quan)
            disc=tot*(10/100)
            finalprice=(tot-disc)+10
        return render(request,'payment.html', {'ci': ct_item, 't': tot,'user':request.user,'disc':disc,'final':finalprice})

