from django.db import models
from django.conf import settings



class Recipe(models.Model):
    recipe_name = models.CharField("レシピ名", max_length=20)
    site = models.CharField("参考サイト", max_length=2048, blank=True, null=False)
    memo = models.TextField("メモ", max_length=1000, blank=True, null=False)
    photo = models.ImageField("写真", upload_to="Media", blank=True, null=False)
    ingredient = models.CharField("材料", max_length=200)
    TYPE = (
        ("スープ", "スープ"),
        ("ご飯", "ご飯"),
        ("おかず", "おかず"),
        ("スイーツ", "スイーツ")
        )
    type = models.CharField("種類", max_length=20, choices=TYPE)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="create_user"
        )
    good_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="いいねしたユーザー",
        blank=True,
        related_name="good_user")
    PUBLIC = (
        ("公開", "公開"),
        ("非公開", "非公開"),
        ("友達のみ", "友達のみ")
        )
    public = models.CharField("公開", max_length=20, choices=PUBLIC, default="非公開")
    #このレシピを元に参考cookを作った人
    quote_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="参考cookユーザー",
        blank=True,
        related_name="quote_user"
        )
    #参考cookを作成したレシピ
    quote_recipe = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="quote_recipe_name",
        )
    #この投稿自体が参考cookかどうか
    quote = models.CharField(max_length=10, default="無し")


    def __str__(self):
        return self.recipe_name

    def summary(self):
        return self.site[:20]
