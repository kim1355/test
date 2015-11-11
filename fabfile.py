from fabric.api import local
def hello():
  local('echo "hello world" ')
