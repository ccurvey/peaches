from django.contrib import admin
from games.models import School, SchoolAlias, Team, Game
# Register your models here.

class SchoolAliasInline(admin.TabularInline):
    model = SchoolAlias

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name','division','mascot')
    list_editable = ('division','mascot')
    search_fields = ('name','mascot')
    inlines = [SchoolAliasInline,]
admin.site.register(School, SchoolAdmin)


admin.site.register(Team)
admin.site.register(Game)
