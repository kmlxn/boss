from django.contrib import admin

from .models import Comment, Topic, Category


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 3


class TopicAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['text', 'number', 'publishers_ip', 'name',
            'image', 'category', 'upvotes', 'downvotes', 'description']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [CommentInLine]
    list_display = ('name', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date', 'category']
    search_fields = ['name']


class TopicInLine(admin.TabularInline):
    model = Topic
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'title', 'description']
    inlines = [TopicInLine]
    list_display = ('name', 'title', 'topic_count')
    search_fields = ['title']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Category, CategoryAdmin)
