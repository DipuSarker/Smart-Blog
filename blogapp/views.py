from django.shortcuts import render
from .models import Author, Category, Post, Subcribe, Contact, Comment, SubComment
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import Http404

# Create your views here.

def index(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        if email:
            Subcribe(email=email).save()

    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    trends = Post.objects.filter(time_upload__gte = week_ago).order_by('-read')
    pop_post = Post.objects.order_by('-read')
    TopAuthors = Author.objects.order_by('-rate')[:4]
    AuthorsPost = [Post.objects.filter(author = author).first() for author in TopAuthors]
    posts = Post.objects.filter(publish=True).order_by('-id')
    all_posts = Paginator(Post.objects.filter(publish=True), 3)
    page = request.GET.get('page')

    try:
        posts = all_posts.page(page)
    except PageNotAnInteger:
        posts = all_posts.page(1)
    except EmptyPage:
        posts = all_posts.page(all_posts.num_pages)

    context = {
        'posts': posts,
        'trends': trends[:5],
        'author_post': AuthorsPost,
        'pop_post': pop_post[:9]
        }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def post(request, id, slug):

    try :
        post = Post.objects.get(pk=id, slug=slug)
    except :
        raise Http404

    post.read += 1
    post.save()

    if request.method == 'POST':
        comm = request.POST.get('comm')
        comm_id = request.POST.get('comm_id')

        if comm_id:
            SubComment(post=post, 
            user=request.user, 
            comm=comm,
            comment = Comment.objects.get(id=int(comm_id))
            ).save()

        else:
            Comment(post=post, user=request.user, comm=comm).save()
    

    comments = []

    for c in Comment.objects.filter(post=post):
        comments.append([c, SubComment.objects.filter(comment=c)])

    context = {
        'comments': comments,
        'post': post,
        'pop_post': Post.objects.order_by('-read')
        }

    return render(request, 'blog-single.html', context)


def contact(request):
    if request.method == 'POST':
        name = f"{request.POST.get('fname')} {request.POST.get('lname')}"
        email = request.POST.get('email')
        mob = request.POST.get('mob')
        mess = request.POST.get('mess')
        
        Contact(name=name, email=email, mob=mob, mess=mess).save()

    return render(request, 'contact.html')


def search(request):
    q = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=q) | Q(overview__icontains=q)).distinct()
    pop_post = Post.objects.order_by('-read')

    context = {
        'posts': posts,
        'title': f'Search result for {q}',
        'pop_post': pop_post[:9]
        }

    return render(request, 'all.html', context)


def view_all(request, query):
    acpt = ['trending', 'popular']
    q = query.lower()

    week_ago = datetime.date.today() - datetime.timedelta(days=7)

    if q in acpt:
        if q == acpt[0]:
            context = {
                'posts' : Post.objects.filter(time_upload__gte = week_ago).order_by('-read'),
                'title': 'Treading Posts',
                'pop_post' : Post.objects.order_by('-read')[:9]
            }

        elif q == acpt[1]:
            context = {
                'posts' : Post.objects.order_by('-read'),
                'title': 'Popular Posts',
                'pop_post' : Post.objects.order_by('-read')[:9]
            }

        else:
            pass

    return render(request, 'all.html', context)
