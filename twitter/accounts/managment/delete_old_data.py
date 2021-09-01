from django.core.management.base import BaseCommand, CommandError
from ..models import UserElementryData
from datetime import timedelta, timezone, datetime


class AutoDeletingRecordAfterTime():
    """Deleting objects of UserElementryData after 10 minutes"""
    def handle(self, *args, **kwargs):
        UserElementryData.objects.filter(created_at___lte=datetime.now()-timedelta(minutes=10))