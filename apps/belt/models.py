from __future__ import unicode_literals

from django.db import models
import bcrypt
from datetime import datetime

# Create your models here.

class TripManager(models.Manager):
    def validate(self,data,user):
        errors = []
        if len(data['destination']) < 1:
            errors.append("Please enter a destination")

        if len(data['plan']) < 1:
            errors.append("Please enter a plan")

        if len(data['start']) < 1:
            errors.append("Please enter a start date!")
        elif datetime.strptime(data['start'], '%Y-%m-%d') < datetime.today():
            errors.append("Travel start date cannot be in the past")

        if len(data['end']) < 1:
            errors.append("Please enter an end date!")
        elif datetime.strptime(data['end'], '%Y-%m-%d') < datetime.strptime(data['start'], '%Y-%m-%d'):
            errors.append("Your trip cannot end before it starts!")

        if len(errors) == 0:
            trip = self.create(destination=data['destination'], plan=data['plan'], start=data['start'], end=data['end'], host=user)
            return trip.id

        return errors

class UserManager(models.Manager):
    def registration(self, data):
        errors =[]
        if len(data['name']) < 3:
            errors.append('Name must contain atleast 3 characters')
        if len(data['username']) < 3:
            errors.append('Username must contain atleast 3 characters')
        if len(data['password']) < 8:
            errors.append('Password must be greater than 8 characters')
        check_username = self.filter(username=data['username'])
        if check_username:
            errors.append('Username has already been taken')
        if data['password'] != data['confirm_password']:
            errors.append('Password and password confirmation fields did not match')
        if len(errors) == 0:
            user = self.create(name=data['name'], username=data['username'], password=bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()))
            return user.id
        return errors

    def verify_login(self, data):
        errors = []
        if len(data['password']) == 0:
            errors.append('Please enter your password')
        check_user = User.objects.filter(username = data['username'])
        if check_user:
            hashed_pw = bcrypt.hashpw(data['password'].encode(), check_user[0].password.encode())
            if check_user[0].password == hashed_pw:
                pass
            else:
                errors.append('Username and Password do not match')
        else:
            errors.append('Username not found')
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    plan = models.TextField()
    start = models.DateField()
    end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    host = models.ForeignKey(User, related_name='trip_host', blank=True, null=True)
    trips = models.ManyToManyField(User, related_name='trip_users')
    objects = TripManager()
