from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

rooms = [
    {'id': 1, 'name': 'Lets go learn python'},
    {'id': 2, 'name': 'Lets go learn java'},
    {'id': 3, 'name': 'Lets go learn c++'},
]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(topic__name__icontains = q)
    room_count = rooms.count() 
    topics = Topic.objects.all()
    messages = Message.objects.filter(room__topic__name__icontains=q)[0:7]
    context = {'rooms':rooms, 'topics':topics, 'rc': room_count, 'messages':messages}
    return render(request, 'base/home.html',context)

def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Login Failed')   

        user = authenticate(request, email=email, password=password)    
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.error(request, 'Invalid Username or Password')   

    context = {'page': page}
    return render(request, 'base/login-register.html',context)

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Some error occurred')

    return render(request, 'base/login-register.html', {'form':form})

def logoutuser(request):
    logout(request)
    return redirect('home')

def userprofile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'users':user, 'rooms':rooms, 'messages':messages, 'topics':topics}
    return render(request, 'base/user-profile.html',context) 

def room(request, pk):
    user = request.user
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    topics = Topic.objects.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room':room, 'messages':messages, 'participants':participants, 'topics':topics, 'users': user}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    page = 'create'
    topics = Topic.objects.all()
    form = RoomForm
    if request.method == 'POST':
        topic_name =  request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
    context = {'form':form, 'topics':topics, 'page': page}
    return render(request, 'base/room-form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")
    
    form = RoomForm(instance=room)
    if request.method == 'POST':
        topic_name =  request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room-form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete-form.html', {'obj':room})

@login_required(login_url='login')
def updateuser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # user = form.save(commit=False)
            # user.username = user.username.lower()
            form.save()
            # login(request, user)
            return redirect('user', pk=user.id)
    return render(request, 'base/update-user.html', {'form':form})


def topic(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(topic__name__icontains = q)
    room_count = rooms.count() 
    topics = Topic.objects.all()
    messages = Message.objects.filter(room__topic__name__icontains=q)
    context = {'rooms':rooms, 'topics':topics, 'rc': room_count, 'messages':messages}
    return render(request, 'base/topic.html', context)

def about(request):
    return render(request, 'base/about.html')
