from django.shortcuts import render, redirect, get_object_or_404
from app01.models import Channel  # 引入新的模型
from app01.utils.form import ChannelForm  # 引入新的表单类

def channel_list(request):
    """报价渠道信息列表视图"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["渠道名称__icontains"] = search_data

    queryset = Channel.objects.filter(**data_dict).order_by("-id")
    context = {
        "search_data": search_data,
        "queryset": queryset,
    }
    return render(request, 'channel_list.html', context)


def channel_add(request):
    """添加报价渠道信息视图"""
    if request.method == "GET":
        form = ChannelForm()
        return render(request, 'channel_form.html', {"form": form, "title": "新建报价渠道信息"})

    form = ChannelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/channel/list/')

    return render(request, 'channel_form.html', {"form": form, "title": "新建报价渠道信息"})


def channel_edit(request, nid):
    """编辑报价渠道信息视图"""
    row_object = get_object_or_404(Channel, id=nid)

    if request.method == "GET":
        form = ChannelForm(instance=row_object)
        return render(request, 'channel_form.html', {"form": form, "title": "编辑报价渠道信息"})

    form = ChannelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/channel/list/')

    return render(request, 'channel_form.html', {"form": form, "title": "编辑报价渠道信息"})


def channel_delete(request, nid):
    """删除报价渠道信息视图"""
    Channel.objects.filter(id=nid).delete()
    return redirect('/channel/list/')