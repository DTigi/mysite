from django.contrib import admin
from .models import Trip, TagPost, Topics

from django.contrib import admin, messages
from django.utils.safestring import mark_safe




# Register your models here.

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'image', 'post_image', 'topic', 'capital', 'tags']
    # exclude = ['tags', 'is_published']
    readonly_fields = ['post_image']
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ['tags']
    list_display = ('title', 'image', 'post_image', 'time_create', 'is_published', 'topic')
    list_display_links = ('title',)
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', 'topic')
    list_per_page = 7
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'topic__name']
    list_filter = ['topic__name', 'is_published']
    save_on_top = True

    @admin.display(description="Изображение")
    def post_image(self, trip: Trip):
        if trip.image:
            return mark_safe(f"<img src='{trip.image.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Trip.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Trip.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title, allow_unicode=True)
    #     super().save(*args, **kwargs)


@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

@admin.register(TagPost)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')
    list_display_links = ('id', 'tag')