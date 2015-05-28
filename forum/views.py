from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
import os
from django.conf import settings

from .forms import *
from .models import Topic, Category


def show_index(request):
    latest_topic_list = Topic.objects.order_by('-pub_date')[:5]
    categories = Category.objects.all()
    context = {
        'latest_topic_list': latest_topic_list,
        'categories': categories,
    }
    return render(request, 'forum/index.html', context)


def show_topic(request, category_name, topic_id):
    category = get_object_or_404(Category, name=category_name)
    topic = get_object_or_404(Topic, id=topic_id, category=category)
    categories = Category.objects.all()
    return render(request, 'forum/topic.html', {'topic': topic, 'categories': categories})


def add_topic(request, category_name):
    if request.method != 'POST':
        return

    category = get_object_or_404(Category, name=category_name)
    form = AddTopicForm(request.POST, request.FILES)

    if form.is_valid():
        topic_number = len(Topic.objects.all()) + 1
        category.topic_set.create(
            text=form.cleaned_data['topic_text'],
            name=form.cleaned_data['topic_name'],
            image=form.cleaned_data['image'],
            pub_date=timezone.now(),
            publishers_ip='127.0.0.0',
            number=topic_number,
        )
        return HttpResponseRedirect(reverse('forum:index'))

    category = get_object_or_404(Category, name=category_name)
    categories = Category.objects.all()
    topics = category.topic_set.order_by('-pub_date')
    context = {
        'topics': topics,
        'category': category,
        'categories': categories,
        'error_message': "Invalid input",
    }

    return render(request, 'forum/category.html', context)



def add_comment_to_topic(request, category_name, topic_id):
    if request.method != 'POST':
        return

    category = get_object_or_404(Category, name=category_name)
    topic = get_object_or_404(Topic, id=topic_id, category=category)

    form = CommentForm(request.POST, request.FILES)

    if not form.is_valid():
        return render(request, 'forum/topic.html', {
            'categories': Category.objects.all(),
            'topic': topic,
            'error_message': "Invalid input.",
        })

    comment_number = topic.comment_set.count() + 1
    topic.comment_set.create(
        text=form.cleaned_data['comment_text'],
        number=comment_number,
        publishers_ip='127.0.0.0',
        pub_date=timezone.now(),
        image=form.cleaned_data['comment_image'],
    )

    return HttpResponseRedirect(reverse('forum:show_topic', args=(category_name, topic.id)))


def show_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    categories = Category.objects.all()
    topics = category.topic_set.order_by('-pub_date')
    context = {
        'topics': topics,
        'category': category,
        'categories': categories,
    }
    return render(request, 'forum/category.html', context)


def add_category(request):
    if request.method != 'POST':
        return

    form = AddCategoryForm(request.POST, request.FILES)

    if not form.is_valid():
        return HttpResponseRedirect(reverse('forum:index', args={'error_message': 'Not valid input'}))
    
    category = Category(
        name=form.cleaned_data['category_name'],
        title=form.cleaned_data['category_title'],
    )
    category.save()

    return HttpResponseRedirect(reverse('forum:index'))