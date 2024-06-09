from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from . import forms
import os

# Create your views here.
def posts_list(request):
    posts = Post.objects.all().order_by('created_at')
    return render(request, 'posts/posts_list.html', { 'posts': posts })

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_detail.html', { 'post': post })

@login_required(login_url="/users/login/")
def post_create(request):
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            # save with user
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
            return redirect('posts:list')
    else:
        form = forms.CreatePost()

    # Add tailwindcss to Form
    form.fields['title'].widget.attrs['class'] = 'title w-full block mb-4 bg-gray-100 border border-gray-300 p-2 mb-4 outline-none'

    form.fields['content'].widget.attrs['class'] = 'description w-full block mb-4 bg-gray-100 sec p-3 h-60 border border-gray-300 outline-none'
    
    form.fields['slug'].widget.attrs['class'] = 'title w-full block mb-4 bg-gray-100 border border-gray-300 p-2 mb-4 outline-none'

    return render(request, 'posts/post_create.html', { 'form': form })

def post_update(request, slug):
    

    post = Post.objects.get(slug=slug)
    # only for author
    if not request.user == post.author:
        return redirect('posts:list')
    form = forms.CreatePost(instance=post)
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES, instance=post)
        # form = forms.CreatePost(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        form.fields['title'].initial = post.title
        form.fields['content'].initial = post.content
        form.fields['slug'].initial = post.slug
    
    # Add tailwindcss to Form
    form.fields['title'].widget.attrs['class'] = 'title w-full block mb-4 bg-gray-100 border border-gray-300 p-2 mb-4 outline-none'

    form.fields['content'].widget.attrs['class'] = 'description w-full block mb-4 bg-gray-100 sec p-3 h-60 border border-gray-300 outline-none'
    
    form.fields['slug'].widget.attrs['class'] = 'title w-full block mb-4 bg-gray-100 border border-gray-300 p-2 mb-4 outline-none'

    return render(request, 'posts/post_update.html', { 'form': form })

def post_delete(request, slug):
    post = Post.objects.get(slug=slug)
    post.image.delete(False)
    post.delete()
    return redirect('posts:list')

def post_search(request):
    query = request.GET.get('search')
    posts = Post.objects.filter(title__icontains=query)
    return render(request, 'posts/posts_list.html', { 'posts': posts })