from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from .forms import PostCreateForm, PostUpdateForm


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 5

def PostListView(request):
    posts = Post.objects.all()
    context = {
        "posts":posts
    }
    return render(request, 'blog/home.html', context)


# class UserPostListView(ListView):
#     model = Post
#     template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     paginate_by = 5

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Post.objects.filter(author=user).order_by('-date_posted')

def UserPostListView(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    context = {
        "posts":posts
    }
    return render(request, 'blog/user_posts.html', context)



# class PostDetailView(DetailView):
#     model = Post

def PostDetailView(request, pk):
    object = Post.objects.get(id = pk)
    context = {
        "object":object
    }
    return render(request, 'blog/post_detail.html', context)



# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

def PostCreateView(request):
    form = PostCreateForm()
    if request.method == "POST":
         form = PostCreateForm(request.POST)
         if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('blog-home')

    context = {
        "form": form
    }
    return render(request, 'blog/post_form.html', context)



# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Post
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False

def PostUpdateView(request, pk):
    post = Post.objects.get(id = pk)
    form = PostUpdateForm(instance = post)
    if request.method == "POST":
        form = PostUpdateForm(request.POST, instance = post)
        if form.is_valid():
            form.save()
            return redirect('blog-home')

    context = {
        "form": form
    }
    return render(request, 'blog/post_form.html', context)

# class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Post
#     success_url = '/'

#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False

def PostDeleteView(request, pk):
    post = Post.objects.get(id = pk)
    post.delete()
    context = {
        "post":post
    }
    return render(request, 'blog/post_delete.html', context)



def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
