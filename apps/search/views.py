import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from posts.models import Post
from .decorators import ajax_required
from posts.forms import PostMediaFormSet, PostForm
# Create your views here.
@login_required
def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')
        try:
            search_type = request.GET.get('type')
            if search_type not in ['posts', 'users']:
                search_type = 'posts'
        except Exception:
            search_type = 'posts'
        
        count = {}
        results = {}
        results['posts'] = Post.objects.none()
        queries = querystring.split()
        for query in queries:
            results['posts'] = results['posts'] | (Post.objects.filter(
                text__icontains=query))
            results['users'] = User.objects.filter(
                Q(username__icontains=query) | Q(
                    first_name__icontains=query) | Q(
                        last_name__icontains=query))
        count['posts'] = results['posts'].count()
        count['users'] = results['users'].count()

        return render(request, 'search/results.html', {
            'hide_search': True,
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'results': results[search_type],
            'mediaformset': PostMediaFormSet(),
            'post_form': PostForm(),       
        })
    else:
        return render(request, 'search/search.html', {'hide_search': True})

