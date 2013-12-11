# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse
from blog.models import Essay,EssayType,Archive,Comment
from django.core.paginator import Paginator
import datetime
from django.db.models import Q
#欢迎页，pageNo=None,etype=None这些都是从urls正则中读取的
#param如果没有就是None
def index(request,pageNo=None,etype=None,keyword=None):
	try:  
	        #文章分页后的页数  
	       	pgNo=int(pageNo)  
	except:  
		pgNo=1  
	try:  
		etype=int(etype)  
	except:  
		etype=None    
	if etype:  
	#查询该类别的文章，exclude表示not in或者!=    
		datas=Essay.objects.all().filter(eType=etype).exclude(title='welcome')    
	elif keyword:  
	#根据关键字查询,title__contains  
	#表示Sql like %+keyword+%  
	#Q对象表示Sql关键字OR查询  
		datas=Essay.objects.all().get(Q(title__contains=keyword)|Q(abstract__contains=keyword)).exclude(title='welcome')  
	else:  
	#查询所有文章  
		datas=Essay.objects.all().exclude(title='welcome')  
	#最近的5篇文章  
	recentList=datas[:5]  
	#数据分页  
	paginator = Paginator(datas, 10)  
	if pgNo==0:  
		pgNo=1  
	if pgNo>paginator.num_pages:  
		pgNo=paginator.num_pages  
	curPage=paginator.page(pgNo)  
	#返回到mian.html模板页  
	return render_to_response('index.html',{  
		'page':curPage,  
		'essay_type':EssayType.objects.all(),  
		'pcount':paginator.num_pages,  
		'recent':recentList,  
		'archives':Archive.objects.all(),  
		#'welcome':Essay.objects.filter(title='welcome')[0]})
		})
	#文章详细信息
def essay_details(request,eid=None):
	#返回文章详细信息或者404页面
	essay=get_object_or_404(Essay,id=eid)
	recentList=Essay.objects.all()[:5]
	#新用户的Session
	if request.session.get('e'+str(eid),True):
		request.session['e'+str(eid)]=False
		#这里可以用一个timer实现，浏览次数保存在内存中，
		#timer定期将浏览次数提交到数据库
		#文章浏览次数+1
	essay.view_count=essay.view_count+1
	essay.save()
	return render_to_response('details.html',{
			'essay':essay,
			'essay_type':EssayType.objects.all(),
			'archives':Archive.objects.all(),
			'date_format':essay.pub_date.strftime('%A %B %d %Y').split(),
			'recent':recentList
			})


#根据关键字来搜索文章   
def search(request):
	if request.method == 'POST':
	#从POST请求中获取查询关键字
		key=request.POST.get('keyword',None)
		return index(request,keyword=key)
	else:
		return index(request)



	#存储用户留言信息
def leave_comment(request,eid=None):
	if request.method == 'POST' and eid:
		uname=request.POST.get('uname',None)
		content=request.POST.get('comment',None)
		email=request.POST.get('email',None)
		#不为空   
		if uname and content and email:
			comment=Comment()
			comment.uname=uname
			comment.content=content
			comment.pub_date=datetime.datetime.now()
			comment.save()
		return index(request)
	return index(request)

