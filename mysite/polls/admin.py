from django.contrib import admin

# 导入问题，选项
from .models import Question,Choice

# Register your models here.

# 问题选项3个
# class ChoiceInline(admin.StackedInline):
# 表格式单行关联对象
class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

# 自定义后台表单
class QuestionAdmin(admin.ModelAdmin):
	# 时间显示在问题前面
	# fields = ['pub_date', 'question_text']

	fieldsets = [
		('题目', {'fields':['question_text']}),
		("时间信息", {'fields':['pub_date'], 'classes':['collapse']}),
	]

	# 添加选项
	inlines = [ChoiceInline]

	# 显示问题的题目，发布日期，是否是最近发布的
	list_display = ('question_text', 'pub_date', 'was_published_recently')

	# 添加侧边过滤器
	list_filter = ['pub_date']

	# 添加搜索框
	search_fields = ['question_text']
admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)