from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.contrib.auth import login,logout,get_user_model,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import SignUpForm,UserLoginForm,PostForm
from .models import Post


#for viewing the post
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'post_list.html',{'posts':posts})

#for detail view
def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request,'post_detail.html',{'post':post})

#to add a new post
@login_required
def post_new(request):
    if request.method =="POST":
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=PostForm()
    return render(request,'post_edit.html',{'form':form})

#to edit the existing post
@login_required
def post_edit(request,pk):
    if pk:
        post = get_object_or_404(Post,pk=pk)
        if post.author != request.user:
            return HttpResponseForbidden()
    else:
        post = Post(author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,'post_edit.html',{'form':form})

@login_required
def post_remove(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request,'post_delete.html',{'post':post})

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        login(request,user)
        return redirect('/')
    return render(request,'login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,new_user)
                    return redirect('/')
    else:
        form = SignUpForm()
    return render(request,'signup.html',{'form':form})
