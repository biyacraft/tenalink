from django.shortcuts import render
import requests


def home(request):
    return render(request, 'pay/home.html')


def payment_with_cart(request):
    obj = {
        "process": "Cart",
        "successUrl": "http://localhost:8000/success",
        "ipnUrl": "http://localhost:8000/ipn",
        "cancelUrl": "http://localhost:8000/cancel",
        "merchantId": "22429",
        "merchantOrderId": "l710.0",
        "expiresAfter": 24,
        "totalItemsDeliveryFee": 19,
        "totalItemsDiscount": 1,
        "totalItemsHandlingFee": 12,
        "totalItemsTax1": 250,
        "totalItemsTax2": 0
    }
    cart = {
        "cartitems": [
            {
                "itemId": "sku-01",
                "itemName": "sample item",
                "unitPrice": 2300,
                "quantity": 1
            },
            {
                "itemId": "sku-02",
                "itemName": "sample item 2",
                "unitPrice": 2300,
                "quantity": 2
            }
        ]
    }
    return render(request, 'pay/index-cart.html', {'obj': obj, 'cart': cart})


def payment_with_express(request):
    obj = {
        "process": "Express",
        "successUrl": "http://localhost:8000/success",
        "ipnUrl": "http://localhost:8000/ipn",
        "cancelUrl": "http://localhost:8000/cancel",
        "merchantId": "SB2367",
        "merchantOrderId": "l710.0",
        "expiresAfter": 24,
        "itemId": 60,
        "itemName": "Billing",
        "unitPrice": 11.0,
        "quantity": 1,
        "discount": 0.0,
        "handlingFee": 0.0,
        "deliveryFee": 0.0,
        "tax1": 0.0,
        "tax2": 0.0
    }
    return render(request, 'pay/index-express.html', {'obj': obj})


def success(request):
    ii = request.GET.get('itemId')
    total = request.GET.get('TotalAmount')
    moi = request.GET.get('MerchantOrderId')
    ti = request.GET.get('TransactionId')
    status = request.GET.get('Status')
    url = 'https://testapi.yenepay.com/api/verify/pdt/'
    datax = {
        "requestType": "PDT",
        "pdtToken": "Q1woj27RY1EBsm",
        "transactionId": ti,
        "merchantOrderId": moi
    }
    x = requests.post(url, datax)
    if x.status_code == 200:
        print("It's Paid")
    else:
        print('Invalid payment process')
    return render(request, 'pay/success.html', {'total': total, 'status': status, })


def cancel(request):
    return render(request, 'pay/cancel.html')


def ipn(request):
    return render(request, 'pay/ipn.html')
