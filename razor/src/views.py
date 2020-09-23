from django.shortcuts import render
import razorpay
from .models import Coffee
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


# Create your views here.
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100
        email = request.POST.get('email')
        # print(name, amount)
        client = razorpay.Client(auth=('rzp_test_NobGhuiQztIFuo', 'WiOKAwsz1TdqgvSHyJhwUts3'))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        # print(payment)
        coffee = Coffee(name=name, email=email, amount=amount, payment_id=payment['id'])
        coffee.save()
        return render(request, 'src/index.html', {'payment': payment})
    return render(request, 'src/index.html/')


@csrf_exempt
def success(request):
    if request.method == 'POST':
        a = request.POST
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        user = Coffee.objects.filter(payment_id=order_id).first()
        user.payment = True
        user.save()
        msg_plain = render_to_string('src/email.txt')
        msg_html = render_to_string('src/email.html')
        send_mail("Your Donation has been received ", msg_plain, settings.EMAIL_HOST_USER, [user.email],
                  html_message=msg_html)
    return render(request, 'src/success.html')
