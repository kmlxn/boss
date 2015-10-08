from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import F
from django.conf import settings

import os
import uuid

from . import forms
from .models import Topic, Category, Comment



def show_index(request):
    latest_topics = list(Topic.objects.order_by('pub_date')[:50])
    hot_topics = sorted(latest_topics, key=lambda x: x.hot(), reverse=True)
    grouped_hot_topics = []

    for i, topic in enumerate(hot_topics):
        if (i % 2 == 0):
            grouped_hot_topics.append([])
        grouped_hot_topics[i // 2].append(topic)

    categories = Category.objects.all()
    context = {
        'grouped_hot_topics': grouped_hot_topics,
        'categories': categories,
    }
    return render(request, 'forum/index.html', context)


def show_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    categories = Category.objects.all()
    grouped_hot_topics = []

    latest_topics = list(category.topic_set.order_by('pub_date')[:50])
    hot_topics = sorted(latest_topics, key=lambda x: x.hot(), reverse=True)

    for i, topic in enumerate(hot_topics):
        if (i % 2 == 0):
            grouped_hot_topics.append([])
        grouped_hot_topics[i // 2].append(topic)

    context = {
        'grouped_hot_topics': grouped_hot_topics,
        'category': category,
        'categories': categories,
    }
    return render(request, 'forum/category.html', context)


def show_or_comment_topic(request, category_name, topic_id):
    category = get_object_or_404(Category, name=category_name)
    topic = get_object_or_404(Topic, id=topic_id, category=category)
    comments = topic.comment_set.order_by('pub_date')
    categories = Category.objects.all()

    if request.method == 'POST':
        form = forms.CommentForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, 'forum/topic.html', {
                'categories': categories,
                'topic': topic,
                'comments': comments,
                'add_comment_form': form,
                'error_message': "Invalid input",
            })

        comment_number = topic.comment_set.count() + 1
        topic.comment_set.create(
            text=form.cleaned_data['comment_text'],
            number=comment_number,
            publishers_ip='127.0.0.0',
            pub_date=timezone.now(),
            image=form.cleaned_data['comment_image'],
        )

        return HttpResponseRedirect(reverse('forum:show_or_comment_topic', args=(category.name, topic.id)))

    else:
        form = forms.CommentForm()

        return render(request, 'forum/topic.html', {
            'topic': topic,
            'categories': categories,
            'comments': comments,
            'add_comment_form': form,
        })


def start_topic(request, category_name=None):
    if request.method == 'POST':
        form = forms.AddTopicForm(request.POST, request.FILES)

        if form.is_valid():
            category = get_object_or_404(Category, name=form.cleaned_data['topic_category'])
            topic_number = len(Topic.objects.all()) + 1
            category.topic_set.create(
                text=form.cleaned_data['topic_text'],
                description=form.cleaned_data['topic_description'],
                name=form.cleaned_data['topic_name'],
                image=form.cleaned_data['topic_image'],
                pub_date=timezone.now(),
                publishers_ip='127.0.0.0',
                number=topic_number,
            )
            return HttpResponseRedirect(reverse('forum:show_category', args=(category.name,)))
        else:
            context = {
                'add_topic_form': form,
                'category': category_name,
                'categories': Category.objects.all(),
                'error_message': 'error',
            }

            return render(request, 'forum/start_topic.html', context)
    else:
        form = forms.AddTopicForm()
        context = {
            'category': category_name,
            'categories': Category.objects.all(),
            'add_topic_form': form,
        }

        return render(request, 'forum/start_topic.html', context)


def add_category(request):
    if request.method != 'POST':
        return

    form = forms.AddCategoryForm(request.POST, request.FILES)

    if not form.is_valid():
        return HttpResponseRedirect(reverse('forum:show_index', args={'error_message': 'Not valid input'}))

    category = Category(
        name=form.cleaned_data['category_name'],
        title=form.cleaned_data['category_title'],
    )
    category.save()

    return HttpResponseRedirect(reverse('forum:show_index'))


def vote_for_topic(request, category_name, topic_id):
    category = get_object_or_404(Category, name=category_name)
    topic = get_object_or_404(Topic, id=topic_id, category=category)

    if request.POST['type'] == 'upvote':
        topic.upvotes += 1
    if request.POST['type'] == 'downvote':
        topic.downvotes += 1

    topic.save()

    if request.POST['referer'] == 'index_page':
        return HttpResponseRedirect(reverse('forum:show_index'))
    if request.POST['referer'] == 'topic_page':
        return HttpResponseRedirect(reverse('forum:show_or_comment_topic', args=(category.name, topic.id)))
    if request.POST['referer'] == 'category_page':
        return HttpResponseRedirect(reverse('forum:show_category', args=(category.name,)))


def vote_for_comment(request, category_name, topic_id, comment_id):
    category = get_object_or_404(Category, name=category_name)
    topic = get_object_or_404(Topic, id=topic_id, category=category)
    comment = get_object_or_404(Comment, id=comment_id, topic=topic)

    if request.POST['type'] == 'upvote':
        comment.upvotes += 1
    if request.POST['type'] == 'downvote':
        comment.downvotes += 1

    comment.save()
    return HttpResponseRedirect(reverse('forum:show_or_comment_topic', args=(category.name, topic.id)))


def upload_image(request):
    form = forms.UploadImageForm(request.POST, request.FILES)

    if not form.is_valid():
        return HttpResponse(status=400)

    url = save_image_and_return_url(form.cleaned_data['image'])
    return HttpResponse(url)


def save_image_and_return_url(file):
    filename = file._get_name()
    dir_name = str(uuid.uuid4())
    os.mkdir(os.path.join(settings.MEDIA_ROOT, 'images', dir_name))
    fd = open(os.path.join(settings.MEDIA_ROOT, 'images', dir_name, filename), 'wb')

    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()

    return settings.MEDIA_URL + 'images/' + dir_name + '/' + filename
