from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Article
from django.views.generic import ListView, DetailView
from .forms import ArticleForm


class ArticleView(View):

    def get(self, request):
        my_data = ":)"
        return render(request, "article_template.html", {"data": my_data})

    def delete(self, request, article_id):
        print(request.GET)
        return HttpResponse('Hello there, deleting {article_id}')
    
    def post(self, request):
        print(request.POST)
        return HttpResponse('Post there')
    

class ArticleListView(ListView):
    model = Article
    context_object_name = 'articlesList'


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'

        
class NewArticleForm(View):
    def get(self, request):
        form = ArticleForm()
        return render(request, 'new_article_form.html', {'form': form})

    def post(self, request):
        form = ArticleForm(request.POST)
            
        if form.is_valid():
            form.save()
            return redirect('all_articles')
        return render(request, 'new_article_form.html', {'form': form})


class EditArticleView(View):
    def get(self, request, id):
        instance = get_object_or_404(Article, id=id)
        form = ArticleForm(instance=instance)
        return render(request, 'edit_article_form.html', {'form': form})
    
    def post(self, request, id):
        instance = get_object_or_404(Article, id=id)
        form = ArticleForm(request.POST, instance=instance)
            
        if form.is_valid():
            form.save()
            return redirect('all_articles')
        return render(request, 'edit_article_form.html', {'form': form})
    
