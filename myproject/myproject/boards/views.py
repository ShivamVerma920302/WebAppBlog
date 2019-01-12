from django.shortcuts import render, redirect
from .models import Board, User, Post
from .forms import NewTopicForm

# Create your views here.
def home(request):
    boards = Board.objects.all()
    return render(request, 'index.html', {'boards': boards})

def board_topics(request,pk):
    board = Board.objects.get(pk=pk)
    return render(request,'topics.html', {'board': board})

def new_topic(request,pk):
    board = Board.objects.get(pk=pk)
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()
        args = {'board': board,
        'form':form}
        return render(request,'new_topic.html', args)