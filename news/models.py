from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rate = models.IntegerField(default=0)

    def update_rating(self):
        # суммарный рейтинг всех комментариев к статьям
        sum_rating = self.post_set.aggregate(post_rating=Sum('post_rate'))
        result_sum_rating = 0
        try:
            result_sum_rating += sum_rating.get('post_rating')
        except TypeError:
            result_sum_rating = 0

        # суммарный рейтинг всех комментариев самого автора
        sum_comment_rating = self.user.comment_set.aggregate(comment_rating=Sum('comment_rate'))
        result_sum_comment_rating = 0
        result_sum_comment_rating += sum_comment_rating.get('comment_rating')

        # суммарный рейтинг каждой статьи автора умноженный на 3
        self.user_rate = result_sum_rating * 3 + result_sum_comment_rating
        # сохраняем результаты в базу данных
        self.save()

    def __str__(self):
        return f'{self.user}. Рейтинг: {self.user_rate}'


class Category(models.Model):
    name_category = models.CharField(max_length=52, unique=True)
    subscribers = models.ManyToManyField(User, null=True, through='CategoryUser')

    # def __str__(self):
    #   return f'Категория {self.name_category}'

    def get_subscribers_emails(self):
        result = set()
        for user in self.subscribers.all():
            result.add(user.email)
        return result
        # subscribers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribed_categories')
    # модуль D9


class CategoryUser(models.Model):  # от Станислава
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    post = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Author;

    created = models.DateTimeField(auto_now_add=True)  # автоматически добавляемая дата и время создания;

    #Post = models.ManyToManyField(Category, through='PostCategory')  # связь «многие ко многим» с моделью Category
    # (с дополнительной моделью PostCategory);
    Post = models.ManyToManyField(Category, through='PostCategory') # заменил название переменной

    title = models.CharField(max_length=150)  # заголовок статьи/новости;

    text = models.TextField()  # текст статьи/новости;

    post_rate = models.IntegerField(default=0)  # рейтинг статьи/новости.

    def __str__(self):
        return f'{self.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    article = 'AR'
    news = 'NE'

    posts = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    choice = models.CharField(max_length=2,  # поле с выбором — «статья» или «новость»;
                              choices=posts,
                              default=news)

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        self.post_rate -= 1
        self.save()

    def preview(self):
        size = 124 if len(self.text) > 124 else len(self.text)
        return self.text[:size] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default=0)

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
