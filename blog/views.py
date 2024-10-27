from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Post, Comment
from django.contrib import messages
from .forms import PostForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from .forms import CommentForm



def home(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, 'Twój wpis został opublikowany!')
                return redirect('home')

        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'home.html', {"posts": posts, 'form': form})
    else:
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'home.html', {"posts": posts})  #


def profile(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=pk)
        posts = Post.objects.filter(user_id=pk).order_by('-created_at')

        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST.get('follow')

            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()
            return redirect('profile', pk=pk)

        return render(request, "profile.html", {"profile": profile, "posts": posts})
    else:
        messages.success(request, "Musisz być zalogowany!")
        return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Teraz jesteś zalogowany!")
            return redirect('home')
        else:
            messages.success(request, "Nieprawdiłowe dane logowania. Spróbuj poownie")
            return redirect('login')

    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "Zostałeś wylogowany")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Zostałeś pomyślnie zarejestrowany!")
            return redirect('home')

    return render(request, "register.html", {'form': form})


def update_user(request):
    try:
        profile_user = Profile.objects.get(user=request.user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)

        if request.method == 'POST':
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Twój profil został zaktualizowany!")
                return redirect('home')
    except Profile.DoesNotExist:
        messages.error(request, "Nie znaleziono profilu.")
        return redirect('home')

    return render(request, "update_user.html", {'profile_form': profile_form})


def delete_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)

        if request.user.username == post.user.username:

            post.delete()

            messages.success(request, "Twoj post zostal usunięty")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, "Nie jesteś właścicielem posta")
            return redirect('home')

    else:
        messages.success(request, "Zaloguj sie aby kontynuowac")
        return redirect(request.META.get("HTTP_REFERER"))


def edit_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if request.user.username == post.user.username:

            form = PostForm(request.POST or None, instance=post)
            if request.method == "POST":
                if form.is_valid():
                    post = form.save(commit=False)
                    post.user = request.user
                    post.save()
                    messages.success(request, ("Twój post został edytowany"))
                    return redirect('home')
            else:
                return render(request, "edit_post.html", {'form': form, 'post': post})

        else:
            messages.success(request, ("Nie jestes właścicielem posta"))
            return redirect('home')

    else:
        messages.success(request, ("Zaloguj się aby kontynuowac"))
        return redirect('home')


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

