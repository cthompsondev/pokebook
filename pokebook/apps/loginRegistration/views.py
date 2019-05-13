from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db.models import F
from apps.loginRegistration.models import *
from django.http import JsonResponse
import bcrypt



def home(request):
    
    return render(request,"loginRegistration/index.html")

def users_create(request):
    password =''
    newuser = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'],
        'alias': request.POST['alias'],
        'birth_date': request.POST['birth_date'],
        'password': request.POST['password'],
        'confpassword': request.POST['confpassword'],
    }
    errors = Users.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = bcrypt.hashpw(newuser['password'].encode(), bcrypt.gensalt())
        user = Users.objects.create(first_name=newuser['first_name'],last_name=newuser['last_name'],alias=newuser['alias'],birth_date=newuser['birth_date'],email=newuser['email'],password=password.decode())
        request.session['email']=user.email
        return redirect('/users/'+str(user.id)+"/pokes")

    

def users_show(request,id):
    if 'email' not in request.session:
        messages.add_message(request, messages.ERROR, "Please Login to view your data")
        return redirect('/')
    user = Users.objects.get(id=id)
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'birth_date': user.birth_date,
        'email': user.email,
        'updated_at': user.updated_at,
    }
    if user.email == request.session['email']:
        return render(request,"loginRegistration/users_show.html",context)
    else:
        user = Users.objects.get(email=request.session['email'])
        messages.add_message(request,messages.ERROR,"You can only view your own user page")
        return redirect('/users/'+str(user.id))
def users_login(request):
    if ('email' not in request.POST) or ('password' not in request.POST):
        messages.add_message(request,messages.ERROR,"You must input your email and password to login")
        return redirect('/')
    user ={
        'email': request.POST['email'],
        'password': request.POST['password']
    }
    try:
        account = Users.objects.get(email=user['email'])
    except:
        messages.add_message(request,messages.ERROR,"Failed login, Try again")
        return redirect('/')
    
    if bcrypt.checkpw(user['password'].encode(), account.password.encode()):
        request.session['email'] = user['email']
        return redirect('/users/'+str(account.id)+'/pokes')
    else:
        return redirect('/')

def logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect('/')


def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken' : Users.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)




def poke_show(request, id):
    try:
        user = Users.objects.get(id=id)
    except:
        messages.add_message(request,messages.ERROR,"Must be logged in to continue")
        return redirect('/')
    
    if 'email' in request.session:
        if request.session['email'] != user.email:
            messages.error(request,'you may only view the pokes page of the logged in user, please login again')
            return redirect('/logout')
    else:
        messages.error(request,'you must be logged in to view a user page')
        return redirect('/')
    
    pokedby = user.poked_users
    #print(pokedby)
    pokers = user.pokers.all().order_by('-count')
    context = {
        'users': Users.objects.exclude(id=id),
        'my': user,
        'pokers':pokers,
        'mypokes': Pokes.objects.filter(poker = user)
    }
    #print(context['pokers'])
    return render(request,'loginRegistration/pokepage.html',context)

def poke_create(request,id):
    #print(request.POST)
    try:
        poker = Users.objects.get(id=id)
        poked = Users.objects.get(id = request.POST['poke'])
    except:
        messages.add_message(request,messages.ERROR,"Poke error, please try again")
        return redirect('/users/'+str(id)+'/pokes')
    
    if Pokes.objects.filter(poker=poker.id,poked=poked.id).exists():
        pokes = Pokes.objects.get(poker=poker.id,poked=poked.id)
        pokes.count = pokes.count +1
        pokes.save()
        #print('count is ', str(Pokes.objects.get(poker=poker.id,poked=poked.id).count))
    else:
        Pokes.objects.create(poker=poker,poked=poked,count=1)

    #pokes = poker.poked_users.all()
    #print(pokes)
    
    return redirect('/users/'+str(id)+'/pokes')