import datetime

from .models import ReadDetail

from django.utils import timezone
from django.db.models import Sum
"""
存放函数
"""

def get_seven_days_read_date(content_type):

	# 获取前七天的阅读数据
	today = timezone.now().date()
	read_nums = []

	dates = []
	# 前七天的阅读次数
	for i in range(7, 0, -1):
		date = today - datetime.timedelta(days=i)

		# 得到的日期
		dates.append(date.strftime('%m/%d'))
		read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
		# 求和
		resault = read_details.aggregate(read_num_sum=Sum('read_nums'))
		read_nums.append(resault['read_num_sum'] or 0)

	return dates, read_nums