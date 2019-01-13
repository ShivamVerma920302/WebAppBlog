from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, User, Post, Topic
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone

# Create your views here.


def home(request):
    boards = Board.objects.all()
    return render(request, 'index.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by(
        '-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    board = Board.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
        args = {'board': board,
                'form': form}
        return render(request, 'new_topic.html', args)


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_post(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
        args = {'topic': topic, 'form': form}
        return render(request, 'reply_post.html', args)


@login_required
def edit_post(request, pk, topic_pk, post_pk):
    post = get_object_or_404(Post, topic=topic_pk, pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.filter(pk=post_pk).update(message = form.cleaned_data.get('message')
            , updated_by=request.user
            , updated_at=timezone.now())
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
        args = {'post': post, 'form': form}
        return render(request, 'edit_post.html', args)
