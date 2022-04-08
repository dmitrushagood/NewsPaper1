
 
# КОНСОЛЬ DJANGO:


from django.contrib.auth.models import User
from news.models import *
1)
dima_user = User.objects.create_user (username = 'dima')
dasha_user = User.objects.create_user (username = 'dasha')

2)
dima = Author.objects.create (user = dima_user)
dasha = Author.objects.create (user = dasha_user)

3)
category_1 = Category.objects.create(name_category = 'Экономика')
category_2 = Category.objects.create(name_category = 'Интернет')
category_3 = Category.objects.create(name_category = 'Культура')
category_4 = Category.objects.create(name_category = 'Музыка')

4)
post_1 = Post.objects.create(post = dima, choice = Post.article, title = 'Это название статьи Димы1', text = 'Это текст  Димы1', post_rate = 5)
post_2 = Post.objects.create(post = dima, choice = Post.article, title = 'Это название новости Димы2', text = 'Это текст Димы2', post_rate = 5)
post_3 = Post.objects.create(post = dasha, choice = Post.article, title = 'Это название статьи Даши', text = 'Это текст  Даши', post_rate = 4)

5)
PostCategory.objects.create(post = post_1, category = category_1)
PostCategory.objects.create(post = post_2, category = category_4)
PostCategory.objects.create(post = post_2, category = category_3)
PostCategory.objects.create(post = post_3, category = category_1)

6)
comment_1 = Comment.objects.create (post = post_1, user = dima.user, text = 'Здоровский коммент_1')
comment_2 = Comment.objects.create (post = post_1, user = dasha.user, text = 'Здоровский коммент_2')
comment_3 = Comment.objects.create (post = post_2, user = dasha.user, text = 'Здоровский коммент_3')
comment_4 = Comment.objects.create (post = post_3, user = dima.user, text = 'Здоровский коммент_4')

7)
Post.objects.get(id=3).dislike()
Post.objects.get(id=2).like()
Comment.objects.get(id=1).like()

Проверка измененных постов\комментариев
Comment.objects.get(id=1).rating
Post.objects.get(id=1).rating
Post.objects.get(id=3).rating

8)
us2 = Author.objects.get(id=2)
чтобы посмотреть суммарный рейтинг комментариев пользователя, можно обратиться к нему напрямую
us2.author.comment_set.aggregate(comment_rating=Sum('comment_rate'))
us2.update_rating()
us2.user_rate

9)
s = Author.objects.order_by('user_rate')
for i in s:
    i.user_rate
    i.user.username

10)
the_best = Post.objects.filter(choice = Post.article).order_by('-post_rate')[0]
    print("Лучшая статья")
    print("Дата:", the_best.created)
    print("Автор:", the_best.post.user.username)
    print("Рейтинг:", the_best.post_rate)
    print("Заголовок:", the_best.title)
    print("Превью:", the_best.preview())


11)