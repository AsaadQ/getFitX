from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewTopicForm
from .models import Board, Topic, Post


# Create your views here.

def boards(request):
    boards = Board.objects.all()
    return render(request,'boards.html', {'boards': boards})


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

#def p (request, board_id):
 #   board = get_object_or_404(Board, pk=board_id)
  #  return redirect('board_topics', board_id=board.pk)