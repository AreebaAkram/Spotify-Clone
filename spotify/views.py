from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import userProfile, song, Comment, Like
from .forms import EditSongForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST


#home page
@login_required(login_url='login') 
def index(request):
    songs = song.objects.all()
    return render (request, 'spotify/index.html', {'songs': songs, 'user':request.user})


@login_required
def profile(request):
    return render(request, 'spotify/profile.html', {'user': request.user})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        country = request.POST['country']
        profile_image = request.FILES.get('profile_image')

        if password == password2:
            if User.objects.filter(email=email).exists():
                return render(request, 'spotify/signup.html', {'error': 'Email already exist'})
            elif User.objects.filter(username=username).exists():
                return render(request, 'spotify/signup.html', {'error': 'Username already exist'})
            else:
                user = User.objects.create_user(username = username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()

                user_profile = userProfile(user=user, profile_image=profile_image, country=country)
                user_profile.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')
    else:
        return render (request, 'spotify/signup.html')
    
@login_required() 
def logout(request):
    auth.logout(request)
    return redirect('login')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'spotify/login.html', {'error': 'Invalid credentials'})

@login_required
def upload_music(request):
    if request.method == 'POST':
        Title = request.POST.get('Title')
        audio = request.FILES.get('audio')  
        song_image = request.FILES.get('song_image') 
        music_uploaded_by = request.user

        music = song.objects.create(
            title=Title,
            audio=audio,
            song_image=song_image,
            user=music_uploaded_by  
        )
        music.save()
        return redirect('/')
    else:
        return render(request, 'spotify/addmusic.html')

@login_required
def edit_song(request, pk):
    song_obj = get_object_or_404(song, pk=pk)
    if request.method == 'POST':
        form = EditSongForm(request.POST, request.FILES, instance=song_obj)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EditSongForm(instance=song_obj)
    return render(request, 'spotify/edit_song.html', {'form': form})

@login_required
def delete(request, pk):
    song_obj = get_object_or_404(song, pk=pk)
    if request.method == 'POST':
        song_obj.delete()
        return redirect('')
    return render(request, 'spotify/delete.html')

@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        song_obj = get_object_or_404(song, pk=pk)
        parent_id = request.POST.get('parent_id')
        
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
            comment = Comment.objects.create(
                user=request.user,
                song=song_obj,
                parent=parent_comment,
                comment=comment
            )
        else:
            comment = Comment.objects.create(
                user=request.user,
                song=song_obj,
                comment=comment
            )
        return redirect('song_comments', pk=pk)
    return render(request, 'spotify/song_comments.html', {'song': song_obj})

@login_required
@require_POST
def toggle_like(request, pk):
    songs = song.objects.get(pk=pk)
    user=request.user
    
    
    if user in songs.likes.all():
        songs.likes.remove(user)
        liked = False
    else:
        songs.likes.add(user)
        liked = True
    return JsonResponse({
        'liked': liked,
        'likes_count': songs.likes.count(),
    })

def search(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        songs = []
        if q:
            songs = song.objects.filter(title__icontains=q)
            return render(request, 'spotify/search.html', {'songs': songs})
        
def song_detail(request, pk):
    songs = get_object_or_404(song, pk=pk)
    return render(request, 'spotify/display.html', {'songs': songs})

def song_comments(request, pk):
    songs = get_object_or_404(song, pk=pk)
    comment = Comment.objects.filter(song=songs)
    return render(request, 'spotify/song_comments.html', {'songs': songs, 'comment': comment})

# def delete_comment(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     if request.method == 'POST':
#         comment.delete()
#         return redirect('add-comment', pk=pk)
#     else:
#         return render(request, 'spotify/delete_comment.html', {'comment': comment})
@login_required
def liked_songs(request):
    liked_songs = song.objects.filter(likes=request.user)
    return render(request, 'spotify/liked_song.html', {'liked_songs': liked_songs})

