import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F, Count
from django.http import JsonResponse
from django.views.generic import TemplateView
from posts.forms import PostMediaFormSet, PostForm
from posts.models import Post


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'feed/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mediaformset'] = PostMediaFormSet()
        context['post_form'] = PostForm()
        return context


@login_required
def retrieve_new_post(request, post_id):
    created_on = Post.objects.filter(
        pk=post_id
    ).values_list(
        'created',
        flat=True
    )
    new_feed = Post.objects.filter(
        feed__user=request.user
    ).order_by('-created').filter(created__gt=created_on).annotate(post_user=F('user__username'),
                                                                   userfname=F('user__first_name'),
                                                                   like_count=Count('likes'),
                                                                   userlname=F('user__last_name')
                                                                   ).values()[:100]

    serialized_response = json.dumps(list(new_feed), cls=DjangoJSONEncoder)
    return JsonResponse(serialized_response, safe=False)
