import email
from enum import unique
from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique= True)
    password = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.email

class AppoUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    massage = models.CharField(max_length=100)
    email = models.EmailField(unique= True)

    def __str__(self) -> str:
        return self.email


class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    education = models.CharField(max_length=50)

    def __str__(self) ->str:
        return self.last_name


class RicruDoctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique= True)
    education = models.CharField(max_length=100)
    massage = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.first_name


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique = True)
    massage = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.first_name