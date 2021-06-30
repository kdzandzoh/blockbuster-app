from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import *
from .decorators import *
from .filters import MovieFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as d_login, logout as d_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import *
from django.contrib import messages

import requests
import datetime
# Create your views here.

key = '85d3db72836e8f6a10edde7b4ae5b960'


def home(request):
    return render(request, template_name='main/home.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def add_movies(request):
    all_movies = []

    if request.method == 'POST':
        if 'AddMovie' in request.POST:
            m_title = request.POST.get('added-movie')
            movie = m_title.split('|')
            print(movie)
            movie_data = Movie(
                name=movie[0],
                description=movie[1],
                year=movie[2],
                genre=movie[3],
                movie_id=movie[4],
                image_url=movie[5]
            )
            messages.success(request, f'Added {movie_data.name} to the collection')
            movie_data.save()
            return redirect('movies')

        elif 'SearchMovie' in request.POST:
            name = request.POST['name']
            url = f'https://api.themoviedb.org/3/search/movie?api_key={key}&language=en-US\
                    &query={name}&page=1&include_adult=false'
            response = requests.get(url)
            movies = response.json()['results']

            count = 0
            current_movies = Movie.objects.values_list('name', flat=True)

            for movie in movies:
                if count == 5:
                    break
                elif movie['title'] not in current_movies:
                    movie_id = movie['id']
                    genres_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=en-US'
                    response = requests.get(genres_url)

                    genres = response.json()['genres']
                    genres_string = ''
                    for g in genres:
                        genres_string += g['name'] + ', '

                        year = 'N/A'

                        try:
                            year = movie['release_date'][:4]
                        except KeyError:
                            print('Release date')

                        movie_data = Movie(
                            name=movie['title'],
                            description=movie['overview'],
                            image_url=movie['poster_path'],
                            genre=genres_string.lstrip().rstrip(', '),
                            movie_id=movie_id,
                            year=year
                        )
                        all_movies.append(movie_data)
                        try:
                            count += 1
                            break
                        except IntegrityError:
                            print(f'Movie data: {movie["title"]}')

    return render(request, template_name='main/add_movies.html', context={'all_movies': all_movies})


def get_movies(request):
    clients = Group.objects.get(name="clients")
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        if clients not in request.user.groups.all():
            messages.error(request, 'You are not authorized to rent movies')
            return redirect('movies')
        movie_title = request.POST.get('rented-movie')
        movie = Movie.objects.get(name=movie_title)
        movie.owner = request.user
        current_date = datetime.date.today()
        rental_length = datetime.timedelta(days=14)
        due_date = current_date + rental_length
        movie.due_date = due_date
        movie.save()
        messages.success(request, f'You rented {movie_title}')
        return redirect('movies')

    all_movies = Movie.objects.all()
    filter = MovieFilter(request.GET, queryset=all_movies)

    choice = request.GET.get('choice')

    if choice == 'All':
        filter = MovieFilter(request.GET, queryset=all_movies)
    elif choice == 'Rented':
        filter = MovieFilter(request.GET, queryset=all_movies.exclude(owner=None))
    else:
        filter = MovieFilter(request.GET, queryset=all_movies.filter(owner=None))

    all_movies = filter.qs

    context = {'all_movies': all_movies, 'filter': filter, 'choice': choice}

    return render(request, template_name='main/movies.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['clients'])
def profile(request):
    form = ClientForm(instance=request.user.client)

    print(dir(form))
    print(form.as_p)

    context = {'form': form}

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=request.user.client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated information')
            form = ClientForm(instance=request.user.client)
            return render(request, template_name='main/profile.html', context={'form': form})

    return render(request, template_name='main/profile.html', context=context)


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        type = request.POST.get('register')
        if type == 'client':
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name='clients')
                user.groups.add(group)
                Client.objects.create(user=user, email=user.email)
                messages.success(request, 'Successfully created a client account for ' + user.username)
                return redirect('login')
            else:
                for field in form:
                    for error in field.errors:
                        messages.error(request, error)

        elif type == 'admin':
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name='admins')
                user.groups.add(group)
                messages.success(request, 'Successfully created an admin account for ' + user.username)
                return redirect('login')
            else:
                for field in form:
                    for error in field.errors:
                        messages.error(request, error)
        else:
            print('Fail')
    context = {'form': form}
    return render(request, template_name='main/register.html', context=context)


@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            d_login(request, user)
            messages.success(request, 'Signed in as ' + username)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username and password combination')
            return redirect('login')

    return render(request, template_name='main/login.html')


def logout(request):
    name = request.user
    d_logout(request)
    messages.success(request, f'Bye {name}!')
    return redirect('home')


def invalid(request):
    return render(request, template_name='main/invalid.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['clients'])
def my_movies(request):
    current_date = datetime.datetime.now()
    if request.method == 'POST':
        if 'Return' in request.POST:
            movie_title = request.POST.get('returned-movie')
            movie = Movie.objects.get(name=movie_title)
            movie.owner = None
            movie.due_date = None
            movie.save()
            messages.success(request, f'You returned {movie_title}')
            return redirect('movies')

    movies = Movie.objects.filter(owner=request.user).order_by('due_date')
    context = {'movies': movies, 'current_date': current_date}
    return render(request, template_name='main/my_movies.html', context=context)
