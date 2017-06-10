# coding:utf-8
from multiprocessing import Process, Queue

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
import json
import redis

from .models import Host, Profile, Task, Report, Attachment
from .forms import TaskForm
                                      

def task(request):
    if request.method == 'POST':
        if 'btn_del' in request.POST:
            t = get_object_or_404(Task, pk=request.POST.get('btn_del'))
            t.delete()
            messages.add_message(request, messages.SUCCESS, '成功删除测试记录')
            return HttpResponseRedirect(reverse_lazy('app:task'))
        if 'btn_stop' in request.POST:
            t = get_object_or_404(Task, pk=request.POST.get('btn_stop'))
            t.terminate()
            messages.add_message(request, messages.SUCCESS, '中止测试任务')
            return HttpResponseRedirect(reverse_lazy('app:task'))
        if 'btn_start' in request.POST:
            t = get_object_or_404(Task, pk=request.POST.get('btn_start'))
            result = t.run.delay(t)
            # t.set_pid(result.task_id)
            report = Report(task=t, tid=result.task_id)
            report.save()
            messages.add_message(request, messages.SUCCESS, '开始测试任务')
            return HttpResponseRedirect(reverse_lazy('app:task'))
    
    page_num = int(request.GET.get('page') or 1)
    status = request.GET.get('status')
    if status:
        tasks = Task.objects.filter(status=status).order_by('-exec_time')
    else:
        tasks = Task.objects.order_by('-exec_time')
    for t in tasks:
        t.result = Report.objects.filter(task=t)
        for r in t.result:
            r.attachs = Attachment.objects.filter(tab_name=r._meta.model_name)
    paginator = Paginator(tasks, 10)
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {'p': page, 'page_range': paginator.page_range}
    return render_to_response('tasks.html', context, context_instance=RequestContext(request))


def step(request):
    print request.GET
    print request.POST
        
    active = request.GET.get('tool')
    form = TaskForm()
    # form.fields["profile"].queryset = Profile.objects.filter(tool=active)
    context = {
               'active': active,
               'form': form,
               }
    
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        host = Host.objects.get(id=request.POST.get('host'))
        prof = Profile.objects.get(id=request.POST.get('profile'))
        dtstr = request.POST.get('exec_time')
        exe_time = timezone.datetime.strptime(dtstr, "%Y-%m-%d %H:%M") - timezone.timedelta(hours=8)
        exe_time = timezone.make_aware(exe_time, timezone.now().tzinfo)
        Task.objects.create(host=host, name=name, desc=desc, profile=prof, exec_time=exe_time)
        messages.add_message(request, messages.SUCCESS, '成功添加任务')
        return HttpResponseRedirect(reverse_lazy('app:task'))
    
    return render_to_response('step.html', context, context_instance=RequestContext(request))


def reports(request, rid):
    t = get_object_or_404(Task, pk=rid)
    reports = Report.objects.filter(task=t).order_by('-c_time')
    for r in reports:
        r.attachs = Attachment.objects.filter(tab_name=r._meta.model_name, tab_id=r.id)
    context = {'reports': reports}
    
    if request.method == 'POST':
        if 'btn_del' in request.POST:
            t = get_object_or_404(Report, pk=request.POST.get('btn_del'))
            t.delete()
            messages.add_message(request, messages.SUCCESS, '成功删除测试结果')
            return HttpResponseRedirect('')
    return render_to_response('reports.html', context, context_instance=RequestContext(request))


def get_log(request):
    rds = redis.StrictRedis()
    index, channel = request.GET.get('index'), request.GET.get('channel')
    len = rds.llen(channel)
    print index, len
    msg = ''.join(rds.lrange(channel, index, len + 1))
    data = json.dumps({"msg": msg, "index": len, "channel": channel}),
    return HttpResponse(data, content_type="application/json")
