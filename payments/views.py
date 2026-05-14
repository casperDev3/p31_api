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
        'server_url': 'https://2dd0-176-104-184-51.ngrok-free.app/api/v1/payments/callback/',
        # URL для отримання результату платежу
        'result_url': 'https://2dd0-176-104-184-51.ngrok-free.app',  # URL для перенаправлення користувача після платежу
    }
    form_html = liqpay.cnb_form(params)
    return render(request, 'payments/pay.html', {'form_html': form_html, 'order_id': order_id})


@csrf_exempt
def liqpay_callback(request):
    try:
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        try:

            # if liqpay.check_signature(data, signature):
            #     # Розшифровуємо дані платежу
            #     payment_data = liqpay.decode_data(data)
            #     print(payment_data)
            #     # Тут можна обробити результат платежу (наприклад, зберегти в базі даних)
            #     return HttpResponse('OK')
            # else:
            #     return HttpResponse('Invalid signature', status=400)

            # Розшифровуємо дані платежу
            payment_data = liqpay.decode_data_from_str(data)
            status = payment_data.get('status')
            order_id = payment_data.get('order_id')

            if status in ['success', 'sandbox']:
                print(f'Payment status: {status}, Order ID: {order_id}')
            else:
                print(f'Payment failed or pending. Status: {status}, Order ID: {order_id}')

            return HttpResponse(f'Payment status: {status}, Order ID: {order_id}', status=200)
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}', status=500)
    except Exception as e:
        print('Error processing callback:', str(e))
        return HttpResponse(f'Error: {str(e)}', status=500)


def success_view(request):
    return HttpResponse('Платіж успішний!')
