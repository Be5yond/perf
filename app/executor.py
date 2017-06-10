# coding:utf-8
import os
import sys
import cStringIO
from fabric.api import local, parallel, run, settings, sudo, env
from fabric.operations import put, get
from fabric.context_managers import cd
from fabric.exceptions import CommandTimeout
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from multiprocessing import Process, Queue
import redis


log_buffer = cStringIO.StringIO()


class RedisFile:
    def __init__(self, key):
        self.key = key
        self.redis = redis.StrictRedis()

        print("inited RedisFile with key:", key)

    def write(self, value):
        self.redis.rpush(self.key, value)
        
    def flush(self):
        pass
    
    def get_txt(self):
        l = self.redis.llen(self.key)
        return ''.join(self.redis.lrange(self.key, 0, l+1))


class Rmt(object):
    def __init__(self, host, user, password):
        self.host_string = '@'.join([user, host])
        self.settings = {'host_string': self.host_string, 'password': password}
    
    def install_pkg(self):
        with settings(**self.settings):
            env.ok_ret_codes.append(1)
            print(env.ok_ret_codes)
            remote_path = run('pwd')
            put(local_path=BASE_DIR+'/static/files/perf.tar', remote_path=remote_path)
            run('tar xvf perf.tar')
            with cd('performance'):
                sudo('rpm -ivh ubench-0.32-1.el6.x86_64.rpm')
    
    def run_ubench(self, q):
        with settings(**self.settings):
            result = run('ubench -m -c')
            q.put(result)
    
    def run(self, command):
        with settings(**self.settings):
            try:
                result = run(command, warn_only=True)
                print(result.failed)
                print(result.succeeded)
                print(result.stderr)
                print(result.stdout)
                run('ls')
            except Exception:
                print 'finish'
            # self.task.log=result

    def run_unixbench(self):
        pass
    
    def run_fio(self):
        pass
    
    def run_spd(self):
        with settings(**self.settings), cd('performance'):
            # with cd('performance'):
            try:
                result = run('python speedtet.py', stdout=log_buffer, stderr=log_buffer)
                print '--------------'
                print result
            except Exception as e:
                print ' in exception --------------'
                print log_buffer.getvalue()
            finally:
                # print log_buffer.getvalue()
                pass
            
    def run_iperf_host(self):
        with settings(**self.settings):
            with cd('performance'):
                run('pwd')
    
    def run_iperf_client(self):
        pass
    
    def run_dstat(self):
        with settings(**self.settings):
            run('dstat -t -n --net-packet 2')

    @parallel
    def demo(self, q):
        with settings(**self.settings):
            # result = run('dstat -t -n --net-packet 1')
            # result = run("python speedtest.py")
            remote_path = run('pwd')
            get(local_path=BASE_DIR+'/static/', remote_path=remote_path+'/performance/*.png')
            result = 132
            q.put(result)

    def demo2(self):
        out = RedisFile("out")
        with settings(**self.settings):
            # log_buffer = cStringIO.StringIO()
            try:
                run('dstat -t -n ', stdout=out)
            except CommandTimeout:
                # print('in demo'+str(id(log_buffer)))
                # print log_buffer.getvalue()
                pass
            
            
if __name__ == '__main__':
    import time
    rds = redis.StrictRedis()
    log_buffer = cStringIO.StringIO()
    h235 = Rmt('123.59.228.235', 'leuser', 'Yangchong123')
    q = Queue()
    p = Process(target=h235.demo2)
    # p2 = Process(target=h235.run_ubench, args=(q,))
    p.start()
    # print p.pid
    # time.sleep(15)
    # p.terminate()
    # h235.demo(q)
    index = 0
    while True:
        len = rds.llen('out')
        for i in rds.lrange('out', index, len):
            print i,
        time.sleep(5)
        index = len
