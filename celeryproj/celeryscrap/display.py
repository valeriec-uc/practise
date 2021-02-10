from django.contrib import admin
from celeryscrap.models import Author


class AuthorDisplay(admin.ModelAdmin):
      list_display = ['author_text','DateOfBirth','author_desc']


admin.site.register(AuthorDisplay,Author)