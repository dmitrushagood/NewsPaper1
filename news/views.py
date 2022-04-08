from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Author, Category
from datetime import datetime
from .search import Posts_filter
from .forms import PostForm
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin


@login_required
def subscribe(request, *args, **kwargs):
    context_dict = {}
    subscribed = request.user.category_set.all()
    context_dict['subscribed'] = subscribed

    if request.method == 'POST':

        if request.POST['from'] == 'post_detail.html':
            post_id = request.POST['post_id']
            post = Post.objects.get(pk=post_id)
            user = request.user
            for cat in post.category.all():
                if user not in cat.subscribers.all():
                    cat.subscribers.add(request.user)
        elif request.POST['from'] == 'subscribe.html':
            print(request.POST)
            cat_id = request.POST['category']
            cat_obj = Category.objects.get(pk=cat_id)
            user = request.user
            cat_obj.subscribers.remove(user)

    return render(request, 'subscribe.html', context=context_dict)


class PostsList(ListView):
    model = Post
    template_name = 'news/Posts.html'
    context_object_name = 'Posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


class Posts_search(ListView):
    model = Post
    template_name = 'news/Posts_search.html'
    context_object_name = 'Posts_search'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = Posts_filter(self.request.GET,
                                         queryset=self.get_queryset())
        return context


class PostDetail(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        flag = False
        #for cat in (context['post']).category.all():
        for cat in (context['post']).Post.all():
            if self.request.user in cat.subscribers.all():
                flag = True
                break
        context['user_is_subscribed'] = flag
        return context
    #ЗДЕСЬ


class PostCreate(PermissionRequiredMixin, CreateView):  # Ограничение прав доступа
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_Post',
                           'news.change_Post')

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        author = Author.objects.get(user_id=user.pk)
        initial['author'] = author
        return initial

    def post(self, request, *args, **kwargs):
        cats_id_list = list(map(int, request.POST.getlist('categorys')))
        categorys = Category.objects.filter(pk__in=cats_id_list)
        my_post = Post(post_type=request.POST['post_type'],
                       text=request.POST['text'],
                       title=request.POST['title'],
                       # author_id=request.POST['author']
                       author=Author.objects.get(pk=request.POST['author']),
                       )
        if check_post_atday(sender=Post, instance=my_post, **kwargs) < 3:
            my_post.save()
            for cat in categorys:
                my_post.categorys.add(cat)
            celery_notify_subscribers.delay(my_post.id)

        return redirect('news')

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): # Ограничение прав доступа
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_Post',
                           'news.change_Post')


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'news/post_delete.html'

    queryset = Post.objects.all()
    success_url = '/news/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    p = request.user.id
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user_id=p)
    return redirect('/news')


#@login_required
#def subscribe_me(request, id):
#    user = request.user.id
#    post_category = Category.objects.filter(post=id)  # по id новости получаем категории
#    for category in post_category:
#        cat = category.name_category
#        if subscribers.objects.filter(user_id=user, subscribe=category).exists():
#            continue
#        else:
#            subscribers.objects.create(user_id=user, subscribe=category)
#            return HttpResponse(f"Вы подписались на новости в категории {cat}")
#    return HttpResponse(f"Вы уже подписаны на новости в категории {cat}")