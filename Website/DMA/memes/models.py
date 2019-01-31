from django.db import models
from django.utils import timezone
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, Adjust
import os
from django.contrib.auth import get_user_model

# Create your models here.

class Post(models.Model):
    title       = models.CharField(max_length=100)
    image       = ProcessedImageField(processors=[ResizeToFit(1080, 1920), Adjust(1.0, 1.0, 1.0, 1.2)],
                                format='JPEG',
                                options={'quality': 60})
    pub_date    = models.DateTimeField('date published', default=timezone.now)
    score       = models.IntegerField(default=0)
    creator     = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name='posts')
    
    def __str__(self):
        return '%s, %s, %s, created by: %s' % (self.title, self.pub_date, self.score, self.creator)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.pk})

class Comment(models.Model):
    text        = models.CharField(max_length=500)
    pub_date    = models.DateTimeField('date published', default=timezone.now)
    creator     = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name='comments')
    post        = models.ForeignKey(Post,
                                on_delete=models.CASCADE,
                                related_name='comments')

    def __str__(self):
        return 'u/%s, %s' % (self.creator, Post.get_absolute_url(self.post))

class Reply(models.Model):
    text        = models.CharField(max_length=500)
    pub_date    = models.DateTimeField('date published', default=timezone.now)
    creator     = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name='replies')
    comment     = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                related_name='replies')

    def __str__(self):
        return 'u/%s, t:%s' % (self.creator, self.text)

class ReactionType(models.Model):
    name        = models.CharField(max_length=20)
    image       = ProcessedImageField(processors=[ResizeToFit(30, 30)],
                                format='JPEG',
                                options={'quality': 70})

    def __str__(self):
        return '%s' % (self.name)

#class Reaction(models.Model):
#    reactiontype= models.ForeignKey(ReactionType,
#                                on_delete=models.CASCADE)
#    creator     = models.ForeignKey(get_user_model(),
#                                on_delete=models.CASCADE)
#    post        = models.ForeignKey(Post,
#                                on_delete=models.CASCADE)