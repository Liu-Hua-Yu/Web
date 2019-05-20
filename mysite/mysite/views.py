from django.http import HttpResponse
from django.shortcuts import render, render_to_response

from django.contrib.contenttypes.models import ContentType
from blog.models import Blog

from read_count.utils import get_seven_days_read_date

def home(request):
	blog_content_type = ContentType.objects.get_for_model(Blog)

	dates, read_nums = get_seven_days_read_date(blog_content_type)

	context = {
		'read_nums':read_nums,
		'dates':dates,
	}
	return render_to_response('home.html', context)
