from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Author


class AuthorDisplay(admin.ModelAdmin):
      list_display = ['author_text','DateOfBirth','author_desc']



admin.site.register(Author,AuthorDisplay)


from .models import Tag


class TagDisplay(admin.ModelAdmin):
    list_display = ['tag_name']


admin.site.register(Tag, TagDisplay)

from .models import Quotes


class QuotesDisplay(admin.ModelAdmin):
    list_display = ['author','quotes_text']


admin.site.register(Quotes, QuotesDisplay)


from .models import Link


class LinkDisplay(admin.ModelAdmin):
    list_display = ['quotes_id','tag_id']


admin.site.register(Link, LinkDisplay)