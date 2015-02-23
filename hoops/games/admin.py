from django.contrib import admin
from games.models import School, Team, Game
# Register your models here.
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name','division','mascot')
    list_editable = ('division','mascot')
admin.site.register(School, SchoolAdmin)

admin.site.register(Team)
admin.site.register(Game)
