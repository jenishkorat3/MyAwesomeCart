import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Product, Contact, Order, OrderUpdate
from collections import defaultdict

def index(request):
    products = Product.objects.all()

    # Group products by category
    category_dict = defaultdict(list)
    for product in products:
        category_dict[product.category].append(product)

    # Chunk products within each category
    def chunked(iterable, n):
        iterable = list(iterable)
        return [iterable[i:i + n] for i in range(0, len(iterable), n)]

    category_chunks = {}
    for category, prods in category_dict.items():
        category_chunks[category] = chunked(prods, 4)

    return render(request, 'shop/index.html', {'category_chunks': category_chunks})

def tracker(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        order_id = request.POST.get('orderId')
        email = request.POST.get('email')

        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if order.exists():
                order_updates = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for update in order_updates:
                    updates.append({
                        'update_desc': update.update_desc,
                        'timestamp': update.timestamp.strftime("%d %b %Y %I:%M %p")
                    })
                if not updates:
                    return JsonResponse({'error': 'This order has not any updates.'}, status=404)
                return JsonResponse({'updates': updates, 'items_json': order[0].items_json}, safe=False)
            else:
                return JsonResponse({'error': 'Order not found or Email id is incorrect.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'shop/tracker.html')

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message')

        contact = Contact(name=name, email=email, phone=phone, subject=subject, message=message)
        contact.save()

    return render(request, 'shop/contact.html')

def checkout(request):
    if request.method == 'POST':
        item_json = request.POST.get('itemJson', '')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address') + ', ' + request.POST.get('address2', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone', '')

        order = Order(items_json=item_json, name=name, email=email, address=address,
                      city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        orderUpdate = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed.")
        orderUpdate.save()
        ThankYou = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'ThankYou': ThankYou, 'id': id})
    return render(request, 'shop/checkout.html')

def productDetail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'shop/productDetail.html', {'product': product})
