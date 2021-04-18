from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from qanda.service import elasticsearch

User = get_user_model()


class Question(models.Model):
    title = models.CharField(max_length=140)
    question = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def as_elasticsearch_dict(self):
        return {
            '_id': self.id,
            '_type': 'doc',
            '_text': f"{self.title}\n{self.question}",
            'question_body': self.question,
            'title': self.title,
            'id': self.id,
            'created': self.created,
        }

    def get_absolute_url(self):
        return reverse('qanda:question_detail', kwargs={'pk': self.id})

    def can_accept_answer(self, user):
        return user == self.user

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update,
                     using=using, update_fields=update_fields)
        elasticsearch.upsert(self)


class Answer(models.Model):
    answer = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.answer[:20]

    class Meta:
        ordering = ('-created',)
