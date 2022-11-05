from django.urls import path, include
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("register/",views.register,name="register"),
    path("about/", views.about,name="about"),
    path("contact/", views.contact, name="contact"),
    path("otp/",views.otp,name="otp"),
    path("doctor/",views.doctor, name="doctor"),
    path("patient/",views.patient,name="patient"),
    path("paymenthandler/",views.paymenthandler,name="paymenthandler"),
    path("paymentfail/",views.paymentfail,name="paymentfail"),
    path("paymentsucces/",views.paymentsucces,name="paymentsucces"),
    path("emergency/",views.emergency,name="emergency"),

]
