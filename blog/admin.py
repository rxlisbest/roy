# -*- coding: UTF-8 -*-
from blog.models import Users,EssayType,Essay,Comment,LevelMsg,Archive  
from django.contrib import admin  
#向Admin中注册一个管理模块  
admin.site.register(Users)  
admin.site.register(EssayType)  
admin.site.register(Essay)  
admin.site.register(Comment)  
admin.site.register(LevelMsg)  
admin.site.register(Archive)
