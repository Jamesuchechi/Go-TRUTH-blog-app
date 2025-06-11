from django import template
import re

register = template.Library()

@register.filter
def urlize_usernames(value):
    if not value:
        return value
    # Find all @username patterns and replace with links
    def replace_username(match):
        username = match.group(1)
        from django.urls import reverse
        profile_url = reverse("user_profile", kwargs={"username": username})
        return f'<a href="{profile_url}" class="text-blue-500 hover:underline">@{username}</a>'
    return re.sub(r'@(\w+)', replace_username, str(value))