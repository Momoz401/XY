# views/job_type_views.py
from django.shortcuts import render, get_object_or_404, redirect
from app01 import models
from app01.models import JobCategoryInfo
from app01.utils.form import BootStrapModelForm


# List View for JobTypeDetailInfo
def job_type_list(request):
    """ List all job types """
    search_query = request.GET.get('q', '')
    if search_query:
        job_types = models.JobTypeDetailInfo.objects.filter(job_name__icontains=search_query)
    else:
        job_types = models.JobTypeDetailInfo.objects.all()

    context = {
        'job_types': job_types,
        'search_query': search_query,
    }
    return render(request, 'job_type_list.html', context)


# ModelForm for JobTypeDetailInfo
class JobTypeDetailInfoModelForm(BootStrapModelForm):
    class Meta:
        model = models.JobTypeDetailInfo
        fields = '__all__'


# Add View for JobTypeDetailInfo
def job_type_add(request):
    """ Add a new job type """
    if request.method == 'GET':
        # 获取所有的二级分类和一级工种
        job_categories = models.JobCategoryInfo.objects.filter(category_level=2)
        parent_jobs = models.JobTypeDetailInfo.objects.filter(job_level=1)

        return render(request, 'job_type_add.html', {
            'job_categories': job_categories,
            'parent_jobs': parent_jobs
        })

    # 处理表单提交
    job_name = request.POST.get('job_name')
    job_level = request.POST.get('job_level')
    job_category_id = request.POST.get('job_category')
    parent_job_id = request.POST.get('parent_job')

    # 获取相关对象
    job_category = models.JobCategoryInfo.objects.get(id=job_category_id)
    parent_job = None if not parent_job_id else models.JobTypeDetailInfo.objects.get(id=parent_job_id)

    # 创建工种
    new_job = models.JobTypeDetailInfo.objects.create(
        job_name=job_name,
        job_level=job_level,
        job_category=job_category,
        parent_job=parent_job
    )

    return redirect('/job_type/list/')


# Edit View for JobTypeDetailInfo
def job_type_edit(request, pk):
    """ Edit an existing job type """
    job_type = get_object_or_404(models.JobTypeDetailInfo, pk=pk)
    if request.method == 'GET':
        form = JobTypeDetailInfoModelForm(instance=job_type)
        return render(request, 'job_type_edit.html', {'form': form})

    form = JobTypeDetailInfoModelForm(request.POST, instance=job_type)
    if form.is_valid():
        form.save()
        return redirect('/job_type/list/')

    return render(request, 'job_type_edit.html', {'form': form})


# Delete View for JobTypeDetailInfo
def job_type_delete(request, pk):
    """ Delete a job type """
    job_type = get_object_or_404(models.JobTypeDetailInfo, pk=pk)
    job_type.delete()
    return redirect('/job_type/list/')
