from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm, UpdateForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class HomeView(ListView):
    model = Post
    template_name = 'blogapp/blog_home.html'
    ordering = ['-post_date']
    paginate_by = 4

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'blogapp/categories.html', {'cats': cats.title().replace('-', ' '), 'category_posts':category_posts})


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'blogapp/article_detail.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogapp/add_post.html'


class AddCategoryView(CreateView):
    model = Category
    #form_class = PostForm
    template_name = 'blogapp/add_category.html'
    fields = '__all__'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddCategoryView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = 'blogapp/update_post.html'
    #fields = ['title', 'title_tag', 'body']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blogapp/delete_post.html'
    success_url = reverse_lazy('home')
