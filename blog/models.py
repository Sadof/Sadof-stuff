from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings



def gen_slug(s):
    new_slug = slugify(s,allow_unicode=True)
    return new_slug + "_" +  str(int(time()))


class Post(models.Model):
    title = models.CharField(max_length=100, blank=False, db_index=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
    )
    slug = models.SlugField(max_length=100, blank=True, unique=True, db_index=True)
    text = models.TextField(blank=False, db_index=True)
    date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField("Tag", related_name="posts", blank=True)

    def save(self,*args,**kwargs):
        if not self.id and not self.slug:
            print(self.slug)
            self.slug = gen_slug(self.title)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('post_detail_url',kwargs={"slug":self.slug})

    def get_delete_url(self):
        return reverse("post_delete_url", kwargs={"slug":self.slug})


    def get_edit_url(self):
        return reverse("post_edit_url", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-date"]





class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def save(self,*args,**kwargs):
        if not self.id and not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag_detail_url',kwargs={"slug":self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={"slug":self.slug})

    def get_edit_url(self):
        return  reverse("tag_edit_url", kwargs={"slug":self.slug})


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    text = models.TextField(blank=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies',on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["-pub_date"]

    def __str__(self):
        return "Comment by {}".format(self.author)



#temporarily account stuff here -_-
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    pic = models.ImageField(blank=True,default="default.png",upload_to="user_profile/")


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profile_url",kwargs={"slug":self.user.username})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


