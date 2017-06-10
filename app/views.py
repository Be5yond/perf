# coding:utf-8
from operator import itemgetter
from multiprocessing import Process
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse
from django.template import RequestContext
from django.db import connection

from .forms import HostForm, ProfForm
from .models import Host, Profile
          

def host(request, hid=None):
    # host detail page
    print request.POST
    if hid:
        h = get_object_or_404(Host, pk=hid)
        if request.method == 'POST':
            if 'btn_install' in request.POST:
                t = request.POST.get('btn_install')
                connection.close()
                Process(target=h.install, args=(t,)).start()
                messages.add_message(request, messages.SUCCESS, '开始安装工具')
                return HttpResponseRedirect('')
        context = {"host": h}
        return render_to_response('host_detail.html', context, context_instance=RequestContext(request))
    
    # add new host
    if request.method == 'POST':
        if 'btn_del' in request.POST:
            t = get_object_or_404(Host, pk=request.POST.get('btn_del'))
            t.delete()
            messages.add_message(request, messages.SUCCESS, '成功删除主机')
            return HttpResponseRedirect('')
        if 'btn_edit' in request.POST:
            t = get_object_or_404(Host, pk=request.POST.get('btn_edit'))
            form = HostForm(request.POST, instance=t)
            if form.is_valid():
                form.save()
            messages.add_message(request, messages.SUCCESS, '成功修改主机')
            return HttpResponseRedirect(reverse_lazy('app:host'))
        else:
            form = HostForm(request.POST)
            if form.is_valid():
                # keys = ('name', 'ip', 'user', 'password')
                # getter = itemgetter(*keys)
                # data = getter(form.data)
                try:
                    # new_host = Host(**dict(zip(keys, data)))
                    form.save()
                except Exception as e:
                    messages.add_message(request, messages.ERROR, e)
                else:
                    messages.add_message(request, messages.SUCCESS, '成功添加新主机')
                return HttpResponseRedirect('')
            else:
                messages.add_message(request, messages.ERROR, form.errors)

    hosts = Host.objects.exclude(status='delete')
    hid = request.GET.get('id')
    if hid:
        t = get_object_or_404(Host, pk=hid)
        form = HostForm(instance=t)
    else:
        form = HostForm()
    form_new = HostForm()
    context = {"form": form, "hosts": hosts, "hid": hid, 'form_new': form_new}
    return render_to_response('hosts.html', context, context_instance=RequestContext(request))


def tool(request):
    tools = Profile.objects.all().order_by('name')

    if request.method == 'POST':
        if 'btn_del' in request.POST:
            t = get_object_or_404(Profile, pk=request.POST.get('btn_del'))
            t.delete()
            messages.add_message(request, messages.SUCCESS, '成功删除测试项')
            return HttpResponseRedirect('')
        if 'btn_edit' in request.POST:
            t = get_object_or_404(Profile, pk=request.POST.get('btn_edit'))
            form = ProfForm(request.POST, instance=t)
            if form.is_valid():
                form.save()
            messages.add_message(request, messages.SUCCESS, '成功修改测试项')
            return HttpResponseRedirect(reverse_lazy('app:tool'))
        else:
            form = ProfForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                except Exception as e:
                    messages.add_message(request, messages.ERROR, e)
                else:
                    messages.add_message(request, messages.SUCCESS, '成功添加新测试项')
                return HttpResponseRedirect('')
            else:
                messages.add_message(request, messages.ERROR, form.errors)

    tid = request.GET.get('id')
    if tid:
        t = get_object_or_404(Profile, pk=tid)
        form = ProfForm(instance=t)
    else:
        form = ProfForm()
    form_new = ProfForm()
    context = {'form': form, 'tools': tools, 'tid': tid, 'form_new':form_new}
    return render_to_response('tools.html', context, context_instance=RequestContext(request))


def shell(request):
    return render_to_response('interact.html', {}, context_instance=RequestContext(request))


def document(request):
    return render_to_response('help.html', {}, context_instance=RequestContext(request))


def channel(request):
    return render_to_response('try.html', {}, context_instance=RequestContext(request))
