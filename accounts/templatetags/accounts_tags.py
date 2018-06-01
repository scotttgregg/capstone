from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def blog_image_or_default(blog):
    if blog.image:
        return mark_safe('<img class="post_img" src="{}" alt="{}">'.format(blog.image.url, blog.alt_text))
    return mark_safe('<img class="post_img" src="{}" alt="Placeholder Image">'.format('/static/accounts/img/placeholder.jpg'))

@register.simple_tag
def profile_image_or_default(user):
    if user.profile_img:
        print(user.profile_img.url)
        return mark_safe('<img class="profile_pic" src="{}" alt="{}">'.format(user.profile_img.url, user.username))
    return mark_safe('<img class="default_profile" src={} alt="Placeholder Image">'.format('/static/accounts/img/profile_default.png'))