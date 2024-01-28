# main/cron.py

from django_cron import CronJobBase, Schedule
from datetime import datetime, timedelta
from .models import Smile, Goal
from django.db import models 
from django.utils import timezone

class ResetFieldsCronJob(CronJobBase):
    RUN_EVERY_MINS = 24 * 60  # Run once a day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.reset_fields_cron_job'

    def do(self):
        # Update SmileInfo fields to zero for entries where a day has passed
        Smile.objects.filter(updated_at__lt=datetime.now() - timedelta(days=1)).update(
            smile_sec=0,
            smile_count=0,
        )
        # Smile.objects.filter(updated_at__lt=datetime.now() - timedelta(days=1)).update(
        #     streak=models.F('streak') + 1
        #     # streak=models.F('streak') + models.Value(1)
        # )
        
        Goal.objects.filter(updated_at__lt=datetime.now() - timedelta(days=1)).update(
            smile_sec=0,
            smile_count=0,
        )
        smile = Smile.objects.get(user=self.request.user)
        current_date = timezone.now().date()
        last_updated_date = smile.streak_time
        if last_updated_date == None:
            last_updated_date = timezone.now().date()
            
        if last_updated_date != current_date:
            smile.streak +=1
            smile.streak_time = timezone.now().date()
        if smile.streak > smile.max_streak:
            smile.max_streak = smile.streak
        
        smile.save()