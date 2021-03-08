from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewTopicForm
from .models import Board, Topic, Post


# Create your views here.

def boards(request):
    boards = Board.objects.all()
    return render(request,'boards.html',{'boards':boards})


def board_topics(request, board_id):
    board= get_object_or_404(Board, pk=board_id)
    return render(request,'topics.html',{'board':board})

def new_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    form = NewTopicForm()
    #if request.method=='POST':
    #subject = request.POST['subject']
      # user = User.objects.first()
       # topic = Topic.objects.create(
        #    subject=subject,
         #   board=board,
         #   created_by=user
        #)
        #post = Post.objects.create(
        #    message=message,
        #     topic=topic,
        #    created_by=user
        #)
        #return redirect('board_topics', board_id=board.pk)
    return render(request, 'new_topic.html',{'board':board,'form':form})

#def p (request, board_id):
 #   board = get_object_or_404(Board, pk=board_id)
  #  return redirect('board_topics', board_id=board.pk)