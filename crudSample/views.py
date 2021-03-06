from django.shortcuts import render,redirect,get_object_or_404
from .models import Comment,Post
from django.utils import timezone
from .forms import PostForm,PostSearchForm,CommentForm 
from django.views.generic.edit import FormView
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    posts=Post.objects.all()
    post_list = Post.objects.all()
    #블로그 객체 세 개를 한페이지로 자르고
    paginator = Paginator(post_list,3)
    #request된 페이지가 뭔지를 알아내고(request 페이지를 변수로 담아내고)
    page = request.GET.get('page')
    #request된 페이지를 얻어온 뒤 return 해준다
    Posts = paginator.get_page(page)
    return render(request,"home.html",{'blogContents':posts,'blogPosts':Posts})


def detail(request,postId):
    post = get_object_or_404(Post,pk=postId) 
    comments = Comment.objects.filter(postId=postId,comment_id__isnull=True)
    re_comments=[]
    for comment in comments:
        re_comments += list(Comment.objects.filter(comment_id=comment.id))
    commentForm = CommentForm()
    return  render(request,'detail.html',{'postContents':post,'comments':comments,'re_comments':re_comments,'commentForms':commentForm})

def create_comment(request, postId):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.postId = Post.objects.get(pk = postId)
            comment.writer = request.user
            comment.pub_date = timezone.now()
            comment.save()
    return redirect('/crudSample/detailPage/'+str(postId))

def create_re_comment(request, postId, comment_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.postId = Post.objects.get(pk = postId)
            comment.writer = request.user
            comment.comment_id = Comment.objects.get(pk = comment_id)
            comment.pub_date = timezone.now()
            comment.save()
    return redirect('/crudSample/detailPage/'+str(postId))

def new(request):
    if request.method == 'POST': #글 작성 후 저장버튼 눌렀을 때
        post_form = PostForm(request.POST,request.FILES)
        if post_form.is_valid():# 이 form을 유효한지 검사후 유효하면 save해줌 (임시저장)
            post = post_form.save(commit = False)#임시저장 해주는 이유는 model에 있는 필드 중 new date를 안 담았음 (commit=False)
            post.writer = request.user
            post.pub_date = timezone.now() 
            post.save()
            return redirect("detailPage",post.id)
    else:
        post_form = PostForm()
        return render(request,'new.html',{'form':post_form})

def edit(request,postId):
    post = get_object_or_404(Post,pk=postId)
    if request.method == 'GET': #수정
        post_form=PostForm(instance=post)
        return render(request,'edit.html',{'edit_post':post_form})
    else:
        post_form = PostForm(request.POST,request.FILES,instance = post)
        if post_form.is_valid():
            post = post_form.save(commit = False)
            post.new_date = timezone.now() # 날짜 생성
            post.save()
        return redirect("detailPage",post.id)

def delete(request,postId):
   deletePost = get_object_or_404(Post,pk=postId)
   deletePost.delete() #삭제해주는 메소드
   return redirect('home')


def deleteComment(request,postId,commentId):
   deleteComment = get_object_or_404(Comment,pk=commentId)
   deleteComment.delete() #삭제해주는 메소드
   return redirect("detailPage",postId)

def deleteAll(request):#관리자일 경우만 전체 게시물 삭제가능하도록 하기
    deleteAll = Post.objects.all()
    deleteAll.delete()
    return redirect('home')
#FormView
class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(body__icontains=searchWord) ).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)

def update_review(request, post_id, comment_id):
    com=Comment.objects.get(id= comment_id)
    com_form=CommentForm(instance=com)
    if request.method == "POST":
        update_form= CommentForm(request.POST, instance = com)
        if update_form.is_valid():
            update_form.save()
            return redirect('/crudSample/detailPage/'+ str(post_id))
    return render(request, 'review_update.html',{'com_form':com_form})
