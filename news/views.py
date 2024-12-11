from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from django_filters.views import FilterView
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def news_list(request):
    post_news = Post.objects.order_by('created_at')
    paginator = Paginator(post_news, 2)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    
    template_name = 'news_list.html'
    return render(request, template_name, {'news': page_obj})  # Изменено на page_obj

def news_detail(request, pk):
    article = get_object_or_404(Post, id=pk)
    return render(request, 'news_detail.html', {'article': article})


def news_search(request):
    post_filter = PostFilter(request.GET, queryset=Post.objects.filter(post_type=Post.NEWS))
    return render(request, 'news_search.html', {'filter': post_filter})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = form.cleaned_data['author']  
            post.save()
            return redirect('news')  
    else:
        form = PostForm()

    return render(request, 'post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect('news')