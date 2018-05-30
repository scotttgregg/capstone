from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def blog_image_or_default(blog):
    if blog.image:
        return mark_safe('<img class="post_img" src="{}" alt="{}">'.format(blog.image.url, blog.alt_text))
    return mark_safe('<img class="post_img" src="{}" alt="Placeholder Image>"'.format('/static/accounts/img/placeholder.jpg'))