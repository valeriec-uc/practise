
from django.urls import path

from celeryscrap import tasks

urlpatterns = [
    path('', tasks.insertdb, name='insertdb'),
]