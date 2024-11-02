# views/job_type_views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from app01 import models
from app01.models import JobCategoryInfo, JobTypeDetailInfo
from app01.utils.form import BootStrapModelForm


# List View for JobTypeDetailInfo
def job_type_list(request):
    """ List all job types """
    search_query = request.GET.get('q', '')
    if search_query:
        job_types = models.JobTypeDetailInfo.objects.filter(job_name__icontains=search_query).order_by('-job_level')
    else:
        job_types = models.JobTypeDetailInfo.objects.all().order_by('job_level')

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
        # 只获取一级工种
        parent_jobs = JobTypeDetailInfo.objects.filter(job_level=1)
        return render(request, 'job_type_add.html', {
            'parent_jobs': parent_jobs
        })

    job_name = request.POST.get('job_name')
    job_level = request.POST.get('job_level')
    parent_job_id = request.POST.get('parent_job')

    # 获取父工种（如果选择了二级工种）
    parent_job = None if job_level == '1' else JobTypeDetailInfo.objects.get(id=parent_job_id)

    # 创建工种
    new_job = JobTypeDetailInfo.objects.create(
        job_name=job_name,
        job_level=job_level,
        parent_job=parent_job
    )

    return redirect('/job_type/list/')


def job_type_edit(request, pk):
    job_type = get_object_or_404(JobTypeDetailInfo, pk=pk)
    if request.method == 'GET':
        parent_jobs = JobTypeDetailInfo.objects.filter(job_level=1)
        return render(request, 'job_type_edit.html', {
            'form': job_type,
            'parent_jobs': parent_jobs
        })

    job_name = request.POST.get('job_name')
    job_level = request.POST.get('job_level')
    parent_job_id = request.POST.get('parent_job')

    # 更新工种信息
    job_type.job_name = job_name
    job_type.job_level = job_level
    job_type.parent_job = None if job_level == '1' else JobTypeDetailInfo.objects.get(id=parent_job_id)

    job_type.save()

    return redirect('/job_type/list/')

# Delete View for JobTypeDetailInfo
def job_type_delete(request, pk):
    """ Delete a job type """
    job_type = get_object_or_404(models.JobTypeDetailInfo, pk=pk)
    job_type.delete()
    return redirect('/job_type/list/')
