from django.contrib import admin
from .models import Post #이때 임포트 해주는 건 models.py에 정의해둔 클래스명

# Register your models here.
admin.site.register(Post)