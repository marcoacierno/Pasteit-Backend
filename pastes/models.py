from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from hashids import Hashids


class Paste(models.Model):
    VISIBILITY = (
        ('public', 'Public'),
        ('unlisted', 'Unlisted'),
        ('private', 'Private'),
    )

    name = models.CharField(max_length=128)
    owner = models.ForeignKey('profiles.Profile', related_name='pastes')
    # TODO: Reduce max_length
    hash_id = models.CharField(max_length=128, unique=True, blank=True, )

    created = models.DateTimeField(help_text=_('Created'), auto_now_add=True, )
    modified = models.DateTimeField(help_text=_('Modified'), auto_now=True, )

    visibility = models.CharField(choices=VISIBILITY, max_length=10)

    content = models.TextField(max_length=settings.MAX_PASTE_CONTENT)

    def save(self, **kwargs):
        if not self.pk:
            super(Paste, self).save(**kwargs)

            self.refresh_from_db()

            hashids = Hashids(min_length=5)

            self.hash_id = hashids.encode(self.pk)
            self.save()

            return

        return super(Paste, self).save(**kwargs)

    def __str__(self):
        return '{}'.format(self.name)
