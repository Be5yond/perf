from fabric.api import local, env, run, settings
# env.hosts = ['leuser@123.59.228.234']


def he():
    with settings(host_string='leuser@123.59.228.235', password='Yangchong123'):
        local('ls')
        result = run("yum install -y gcc perl")
        print(result)
print __name__


if __name__ == '__main__':
    he()
