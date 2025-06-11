from .models import Category, Tag

def common_context(request):
    return{
        'categgories': Category.objects.all(),
        'tags': Tag.objects.all()
    }