from django import template

register = template.Library()

# filter that will be used in quiz_app_question.html template to display range options
# could use range function inside the template itself, but its available only in 4.3 Django and mine is currently 4.2.2.
@register.filter
def custom_range(value, arg):
    # Implement your custom filter logic here
    return range(value, arg)
