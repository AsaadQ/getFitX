from datetime import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewTopicForm, PostForm
from .models import Board, Topic, Post


# Create your views here.

def boards(request):
    boards = Board.objects.all()
    post =  Post.objects.all().count()
    return render(request,'boards.html', {'boards': boards, 'post': post})


def board_topics(request, board_id):
    board= get_object_or_404(Board, pk=board_id)
    return render(request,'topics.html', {'board': board})


@login_required
def new_topic(request,board_id):
    board = get_object_or_404(Board,pk=board_id)
    # user = User.objects.first()
    if request.method == "POST":
        form =NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                created_by = request.user,
                topic=topic

            )
            return redirect('board_topics',board_id=board.pk)
    else:
        form = NewTopicForm()

    return render(request,'new_topic.html',{'board':board,'form':form})


def topic_posts(request, board_id, topic_id):
    topic = board = get_object_or_404(Topic,board__pk=board_id , pk=topic_id)

    return render(request, 'topic_posts.html', {'topic':topic})

@login_required
def reply_topic(request, board_id,topic_id):
    topic = get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
    if request.method == "POST":
        form =PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()


            return redirect('topic_posts',board_id=board_id, topic_id = topic_id)
    else:
        form = PostForm()
    return render(request,'reply_topic.html',{'topic':topic,'form':form})