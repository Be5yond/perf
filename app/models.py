# coding:utf-8
import os
from django.db import models
from model_utils.models import StatusModel
from model_utils import Choices
import time
from django.utils import timezone

# Create your models here.
import cStringIO
from fabric.api import run, settings, sudo, env, local
from fabric.operations import put, get
from fabric.context_managers import cd
from celery import Celery
from .leyig import LeYig
from .executor import RedisFile
import redis
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


app = Celery('tasks', broker='redis://localhost:6379/0')
yig = LeYig()
rds = redis.StrictRedis()


TOOLS = {'ubench': 'rpm -ivh ubench-0.32-1.el6.x86_64.rpm',
         'unixbench': 'yum install -y perl gcc SDL-devel mesa-libGL-devel',
         'fio': 'yum install libaio && rpm -ivh fio-2.0.10-1.el6.rf.x86_64.rpm',
         'iperf': 'yum install iperf && rpm -ivh epel-release-6-8.noarch.rpm',
         'speedtest': '',
         }


class Host(StatusModel):
    STATUS = Choices('idle', 'error' 'testing', 'offline', 'delete')
    name = models.CharField(max_length=255, verbose_name="主机名称")
    ip = models.GenericIPAddressField(unique=True, verbose_name="IP地址")
    info = models.TextField(default='')
    user = models.CharField(max_length=16, verbose_name="用户名")
    password = models.CharField(max_length=16, verbose_name="密码")

    def __unicode__(self):
        return self.name+'_'+self.ip
    
    def get_setting(self):
        host_string = '@'.join([self.user, str(self.ip)])
        return {'host_string': host_string, 'password': self.password}
    
    def shell(self, command):
        self.status = 'installing'
        self.save()
        with settings(**self.get_setting()):
            try:
                result = run(command)
            except Exception as e:
                result = e
            return result
    
    def set_status(self, status):
        self.status = status
        self.save()
        

class Tool(models.Model):
    name = models.CharField(max_length=255, verbose_name="工具名称")
    platform = models.CharField(max_length=255, verbose_name="适用系统平台")
    prefix = models.CharField(max_length=255, verbose_name="运行命令")
    suffix = models.CharField(max_length=255, verbose_name="运行命令后缀", default='')
    install = models.CharField(max_length=255, verbose_name="工具安装命令", default='')
    detect = models.CharField(max_length=255, verbose_name="检查是否安装命令", default='')
    delete = models.CharField(max_length=255, verbose_name="工具卸载命令", default='')
    
    def __unicode__(self):
        return self.name


class Profile(models.Model):
    name = models.CharField(max_length=255, verbose_name="测试模版名称", unique=True)
    desc = models.CharField(max_length=255, verbose_name="测试模版说明", default='')
    tool = models.ForeignKey(Tool, verbose_name="测试工具")
    params = models.CharField(max_length=255, verbose_name="工具命令参数", default='')
    c_time = models.DateTimeField(auto_now_add=True,)
    
    def __unicode__(self):
        return self.name
    
    def command(self):
        return ' '.join([self.tool.prefix, self.params, self.tool.suffix])


class Task(StatusModel):
    STATUS = Choices('wait', 'running', 'finish', 'error')
    name = models.CharField(max_length=255, verbose_name="任务名称", default='')
    desc = models.CharField(max_length=255, verbose_name="任务描述", default='')
    host = models.ForeignKey(Host, verbose_name="目标主机")
    profile = models.ForeignKey(Profile, verbose_name="测试模版")
    exec_time = models.DateTimeField(auto_now_add=True, verbose_name="执行时间")
    result = models.CharField(max_length=16, default='')
    log = models.TextField(default='')

    def __unicode__(self):
        return self.host.name +'_'+ self.profile.name
    
    def detect(self):
        with settings(**self.host.get_setting()), cd('performance'):
            try:
                run(self.profile.tool.detect)
            except Exception as e:
                pass
            
    @app.task()
    def run(self):
        log_buffer = cStringIO.StringIO()
        log_buffer = RedisFile('log'+str(self.id))
        self.status = 'wait'
        self.save()
        retry = 0
        
        while timezone.now() < self.exec_time or not Host.objects.get(id=self.host.id).status == 'idle':
            print '-----------in wait status-----------'
            print '[Host] ' + Host.objects.get(id=self.host.id).status
            print '[now]'+str(timezone.now())
            print '[exec_time]'+str(self.exec_time)
            print '-----------in wait status-----------'
            time.sleep(60)
            retry += 1
            if retry == 120:
                self.status = 'error'
                self.log = 'Maximum retry limit reached'
                self.save()
                return
        
        self.status = 'running'
        self.exec_time = timezone.now()
        self.host.set_status('testing')
        self.save()
        with settings(**self.host.get_setting()):
            print '-----------in running status-----------'
            try:
                ret = run(self.profile.tool.detect, warn_only=True)
                if ret.failed:
                    remote_path = run('pwd')
                    put(local_path=BASE_DIR+'/static/files/perf.tar', remote_path=remote_path)
                    run('tar xvf perf.tar')
                    with cd('performance'):
                        sudo(self.profile.tool.install, warn_only=True)
                with cd('performance'):
                    run(self.profile.command(), stdout=log_buffer, warn_only=True)
            except Exception as e:
                print '--------------- except --------------'
                self.status = 'error'
                self.log = e
                print e
            else:
                print '--------------- else --------------'
                self.status = 'finish'
            finally:
                print '--------------- finally --------------'
                if not self.status == 'finish':
                    self.status = 'error'
                self.log = log_buffer.get_txt()
                self.host.set_status('idle')
                self.save()
                self.gen_report()
                rds.delete('log'+str(self.id))
    
    def set_pid(self, tid):
        self.report.tid = tid
        self.report.save()
        
    def terminate(self):
        try:
            tid = Report.objects.filter(task=self).order_by('-c_time')[0].tid
            app.control.revoke(tid, terminate=True)
        except Exception as e:
            print e
        else:
            self.host.set_status('idle')
            self.status = 'finish'
            self.log += 'program manually terminated by user'
            self.save()

    def gen_report(self):
        print '-------in gen_report-----------'
        report = Report.objects.filter(task=self).order_by('-c_time')[0]
        report.command = self.profile.command()
        report.log = self.log
        report.save()
        
        with open(BASE_DIR+'/static/temp/log.txt', 'w') as f:
            f.write(self.log)
        res = yig.upload_url(BASE_DIR+'/static/temp/', 'log.txt',)
        for k, v in res.items():
            Attachment(name=k, url=v, tab_name=report._meta.model_name, tab_id=report.id).save()
        
        if self.profile.tool.name == 'fio':
            with settings(**self.host.get_setting()):
                remote_path = run('pwd')
                get(local_path=BASE_DIR+'/static/temp/', remote_path=remote_path+'/performance/fio.tar')
            res = yig.upload_url(BASE_DIR+'/static/temp/', 'fio.tar',)
            for k, v in res.items():
                Attachment(name=k, url=v, tab_name=report._meta.model_name, tab_id=report.id).save()
        

class Report(models.Model):
    task = models.ForeignKey(Task)
    tid = models.CharField(max_length=255, blank=True, null=True, default=None)
    command = models.TextField(verbose_name="执行命令", default='')
    log = models.TextField(default='')
    c_time = models.DateTimeField(auto_now_add=True, )
    
    def __unicode__(self):
        return str(self.tid)
    

class Attachment(models.Model):
    name = models.CharField(max_length=255, verbose_name="附件名称", default='')
    url = models.CharField(max_length=255, verbose_name="附件地址", default='')
    tab_name = models.CharField(max_length=64, verbose_name="目标表名称")
    tab_id = models.IntegerField(verbose_name="目标表id")
    c_time = models.DateTimeField(auto_now_add=True, )
    
    def __unicode__(self):
        return self.name
