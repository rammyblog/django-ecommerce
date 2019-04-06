from django.shortcuts import render, redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models  import User
from accounts.models import UserProfile
from django.db.models import Q

def order_create(request):
    cart = Cart(request)
    try:
        user = UserProfile.objects.filter(user=request.user).filter(default_address=True).first()
        if user == None:
            print(user)
            return redirect(reverse('accounts:user_profile'))
            
    except AttributeError as e:
        return redirect(reverse('accounts:user_profile'))
    
    # user = get_object_or_404(UserProfile, user=request.user)
    print(user)
    user_details = {'first_name':user.user.first_name,'last_name':user.user.last_name, 'email':user.user.email, 'address':user.address, 
                        'postal_code':user.postal_code, 'city':user.city}
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, initial=user_details)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user.user
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id']=order.id
            return redirect(reverse('payment:process'))
            # return render(request, 'orders/order/created.html', {'order':order})
    else:
        form = OrderCreateForm(initial=user_details)
    return render(request, 'orders/order/create.html', {'cart':cart, 'form':form, 'user':user})

        
# @staff_member_required
@login_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order':order})
