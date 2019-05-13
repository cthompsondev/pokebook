from django.db import models
import re
import datetime
from dateutil.relativedelta import relativedelta

class RegistrationManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "User first name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "User last name should be at least 2 characters"
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias should be at least 2 characters"
        if not re.match(r'\b[\w.-]+@[\w\.-]+\.\w{2,4}\b', postData['email']):
            errors['email'] = "Email not valid"
        if Users.objects.filter(email=postData['email']).count() > 0:
            errors['email'] = "Email not unique"
        try:
            if datetime.datetime.strptime(postData['birth_date'],'%Y-%m-%d') > datetime.datetime.today():
                errors['birth_date'] = "User birthday must be before today"
            if datetime.datetime.strptime(postData['birth_date'],'%Y-%m-%d') +relativedelta(years=13) > datetime.datetime.today():
                errors['age'] = "Users must be atleast 13 years old to register"
        except:
            errors['birth_date'] = "Birth day must be selected from the calender"
        
        if not postData['password'] == postData['confpassword']:
            errors['password_match'] = "Passwords do not match"
        if len(postData['password']) < 8:
            errors['password_length'] = "Password should be atleast 8 characters"

        return errors


class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    birth_date = models.DateField()
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poked_users = models.ManyToManyField('self',through='Pokes',through_fields=('poker','poked'),symmetrical=False)
    objects = RegistrationManager()
    
class Pokes(models.Model):
    poker = models.ForeignKey('Users',on_delete=models.CASCADE)
    poked = models.ForeignKey('Users',on_delete=models.CASCADE,related_name="pokers")
    count = models.IntegerField()
