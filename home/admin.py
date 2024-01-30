from django.contrib import admin
from .models import Smile, Goal, Level, Activity, Community, UserJoinedCommunity,CommPost, Friend

# Register your models here.
admin.site.register(Smile)
admin.site.register(Goal)
admin.site.register(Level)
admin.site.register(Activity)
admin.site.register(Community)
admin.site.register(UserJoinedCommunity)
admin.site.register(CommPost)
admin.site.register(Friend)