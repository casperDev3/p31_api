from django.shortcuts import render
import uuid
from django.http import HttpResponse
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from liqpay import LiqPay


def pay_view(request):
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    order_id = str(uuid.uuid4().hex[:8])  # Генеруємо унікальний ID замовлення
    params = {
        'action': 'pay',
        'amount': '1',  # Сума платежу
        'currency': 'UAH',  # Валюта
        'description': 'Оплата за послугу',
        'order_id': order_id,
        'version': '3',
        'sandbox': 1,  # Використовуємо тестовий режим
        'server_url': 'http://localhost:8000/payments/callback/',  # URL для отримання результату платежу
        'result_url': 'http://localhost:8000/payments/result/',  # URL для перенаправлення користувача після платежу
    }
    form_html = liqpay.cnb_form(params)
    return render(request, 'payments/pay.html', {'form_html': form_html})


@csrf_exempt
def liqpay_callback(request):
    data = request.POST.get('data')
    signature = request.POST.get('signature')
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    try:
        if liqpay.check_signature(data, signature):
            # Розшифровуємо дані платежу
            payment_data = liqpay.decode_data(data)
            print(payment_data)
            # Тут можна обробити результат платежу (наприклад, зберегти в базі даних)
            return HttpResponse('OK')
        else:
            return HttpResponse('Invalid signature', status=400)
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)


def success_view(request):
    return HttpResponse('Платіж успішний!')
