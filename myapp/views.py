
from email import message
from random import randint
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from myapp.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import razorpay
# Create your views here.


def index(request):
    return render (request, "index.html")

def contact(request):
    if request.method== "GET":
        return render (request, "contact.html")
    else:
        global user_appo
        user_appo = {
            "first_name" : request.POST["fname"],
            "last_name" : request.POST["lname"],
            "massage" : request.POST["massage"],
            "email" : request.POST["appo_email"]
        }
        
        AppoUser.objects.create(
            first_name = user_appo["first_name"],
            last_name = user_appo["last_name"],
            massage = user_appo["massage"],
            email = user_appo["email"]
    )
        return render( request,"index.html")
def about(request):
    return render(request, "about.html")

def register(request):
    if request.method=="GET":
        return render(request,"register.html")
    else:
        global user_data
        user_data = {
            "first_name":request.POST["fname"],
            "last_name":request.POST["lname"],
            "email":request.POST["email"],
            "password":request.POST["pass"],
            "re_password":request.POST["re_pass"]
        }
        if request.POST["pass"] == request.POST["re_pass"]:
            global c_otp
            c_otp = randint(1000,9999)
            message = f"Your OTP is {c_otp}"
            send_mail("registration's process",message, settings.EMAIL_HOST_USER,[user_data["email"]])
            return render(request, "otp.html",{"msg":"Check Your MailBox:)"})
        else:
            return render(request, "register.html",{"msg":"Password Are Wrong Please Try Again"})

def otp(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        global c_otp
        if int(request.POST["u_otp"]) == c_otp:
            User.objects.create(
                first_name = user_data["first_name"],
                last_name = user_data["last_name"],
                email = user_data["email"],
                password = user_data["password"]  
            )
            return render(request, "index.html",{"msg": "Your registration are succesful!!!"})


def doctor(request):
    if request.method == "GET":
        return render(request, "doctor.html")

    else:
        doctor_data = {
            "first_name":request.POST["fname"],
            "last_name":request.POST["lname"],
            "email":request.POST["email"],
            "education":request.POST["education"],
            "massage":request.POST["massage"],
        }
        RicruDoctor.objects.create(
            first_name=doctor_data["first_name"],
            last_name=doctor_data["last_name"],
            email=doctor_data["email"],
            education = doctor_data["education"],
            massage = doctor_data["massage"],
        )

        return render(request, "index.html")

 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
def patient(request):
    if request.method == "GET":
        return render(request, "patient.html")
    
    else:
         currency = 'INR'
    amount = 50000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'pay.html', context=context)

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsucces.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

        patient_data = {
            "first_name" : request.POST["fname"],
            "last_name" : request.POST["lname"],
            "email" : request.POST["pat_email"],
            "massage" :request.POST["massage"],
        }
        Patient.objects.create(
            first_name = patient_data["first_name"],
            last_name = patient_data["last_name"],
            email = patient_data["email"],
            massage = patient_data["massage"]
        )

        return render(request, "index.html")



def paymentfail(request):
    return render(request,"paymentfail.html")

def paymentsucces(request):
    return render(request,"paymentsucces.html")

def emergency(request):
    return render(request,"emergency.html")



