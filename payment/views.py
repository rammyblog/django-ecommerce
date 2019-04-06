import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {'submit_for_settlement': True}
        })
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done', order.id) 
        else:
            
            return redirect('payment:canceled', order.id)
    else:
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', {
            'order':order,
            'client_token':client_token
        })

def payment_done(request, order_id):
    order = get_object_or_404(Order, id = order_id)
    context = {'order':order}
    return render(request, 'payment/done.html', context)

def payment_canceled(request,order_id):
    order = get_object_or_404(Order, id = order_id)
    context = {'order':order}
    return render(request, 'payment/canceled.html', context)

def payment_process_again(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {'submit_for_settlement': True}
        })
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done', order.id) 
        else:
            return redirect('payment:canceled', order.id)
    else:
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/new_payment.html', {
            'order':order,
            'client_token':client_token
        })
