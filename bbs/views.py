from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST
from .utils import login_required
from django.utils.decorators import method_decorator
from .models import Article, Comment
from .parameters import CURRENT_USER
from .forms import ArticleForm
from django.core.paginator import Paginator, EmptyPage


@login_required
def index(request, **kwargs):
    # 主页，直接跳转到文章列表的第一页
    return redirect(reverse('bbs:article', kwargs={'page': 1}))


@method_decorator(login_required, name='dispatch')
class PublishView(View):
    # 发表文章

    # get方法，直接渲染页面，传入error_message
    def get(self, request, error_message=None, **kwargs):
        if error_message:
            context = {
                'error_message': error_message
            }
        else:
            context = {}
        return render(request, 'bbs/publish.html', context=context)

    # post方法，处理用户提交的文章信息，根据处理结果做不同的返回
    def post(self, request, **kwargs):
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            author = kwargs.get(CURRENT_USER)
            article = Article(title=title, content=content, author=author)
            article.save()
            return self.get(request, error_message='发表成功！')
        else:
            error_message = form.errors.popitem()[1][0]
            return self.get(request, error_message)


@login_required
def article(request, page, **kwargs):
    # 文章列表
    articles = Article.objects.all().order_by('-publish_time')  # 取出所有文章，按照发表时间排列（新到旧）
    # 下面是django分页的一些设置，基本都是固定的
    paginator = Paginator(articles, 10)  # 设置每一页显示几条  创建一个panginator对象

    try:
        current_num = page
        if not current_num: current_num=1# 当你在url内输入的?page = 页码数  显示你输入的页面数目 默认为第1页
        articles = paginator.page(current_num)
    except EmptyPage:
        return redirect(reverse('bbs:article', kwargs={'page': 1})) # 当你输入的page是不存在的时候跳转到第1页

    if paginator.num_pages > 11:  # 如果分页的数目大于11
        if current_num - 5 < 1:  # 你输入的值
            pageRange = range(1, 11)  # 按钮数
        elif current_num + 5 > paginator.num_pages:  # 按钮数加5大于分页数
            pageRange = range(current_num - 5, current_num + 1)  # 显示的按钮数

        else:
            pageRange = range(current_num - 5, current_num + 6)  # range求的是按钮数   如果你的按钮数小于分页数 那么就按照正常的分页数目来显示

    else:
        pageRange = paginator.page_range  # 正常分配

    context = {
        'articles': articles,
        'pageRange': pageRange,
    }
    return render(request, 'bbs/article.html', context=context)


@login_required
def detail(request, id, **kwargs):
    # 文章详情页面
    # 根据文章ID（从url中获取）获取文章以及其所有评论
    article = get_object_or_404(Article, pk=id)
    comments = article.comment_set.all().order_by('-publish_time')
    context = {
        'article': article,
        'comments': comments,
    }
    return render(request, 'bbs/detail.html', context=context)


@login_required
@require_POST
def comment(request, id, **kwargs):
    # 发表评论（展示评论在文章详情页中）
    # 根据文章ID（从url中获取）获取针对的文章
    # 获取request中的评论内容，存入数据库中即可
    article = get_object_or_404(Article, pk=id)
    current_user = kwargs.get(CURRENT_USER)
    comment_content = request.POST['commentContent']
    comment = Comment(article=article, content=comment_content, author=current_user)
    comment.save()
    # 添加完成后返回当前文章详情界面
    return redirect(reverse('bbs:detail', kwargs={'id':id}))