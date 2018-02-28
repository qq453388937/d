# -*- coding:utf-8 -*-

from django.core.files.storage import Storage
from django.conf import settings


class FastDFSStorage(Storage):
    """实现django上传静态文件到fdfs"""

    def __init__(self, client_conf=None, server_ip=None):
        """初始化"""
        if client_conf is None:
            # client_conf = './client/conf'
            client_conf = settings.CLIENT_CONF
        if server_ip is None:
            # server_ip = 'http://192.168.247.128:8888/'
            server_ip = settings.SERVER_IP
        self.client_conf = client_conf
        self.server_ip = server_ip

    def _open(self, name, mode='rb'):
        """打开文件时使用,此处不是打开，是存储"""
        pass

    def _save(self, name, content):
        """content.read() 获取byte字节数据
        1. import fdfs_client.client module
        2. instantiate class Fdfs_client
        3. call memeber functions

         from fdfs_client.client import *
         client = Fdfs_client('/etc/fdfs/client.conf')
         ret = client.upload_by_filename('test')
         ret
            {'Group name':'group1','Status':'Upload successed.', 'Remote file_id':'group1/M00/00/00/
            wKjzh0_xaR63RExnAAAaDqbNk5E1398.py','Uploaded size':'6.0KB','Local file name':'test'
            , 'Storage IP':'192.168.243.133'}
        """
        from fdfs_client.client import Fdfs_client
        # 1. 创建client对象，参数是client.conf
        # client = Fdfs_client('./client.conf')  # 耦合性
        # client = Fdfs_client(self.client_conf)  # 耦合性
        client = Fdfs_client(settings.CLIENT_CONF)
        # 2.调用client.upload_by_buffer(file)
        buffer = content.read()
        try:
            ret = client.upload_by_buffer(buffer)
        except Exception as e:
            print(e)  # 方便调试
            raise  # 捕获到什么异常就抛出异常，将错误暴露出来
        if ret.get('Status') == 'Upload successed.':
            # 上传成功！
            file_id = ret.get('Remote file_id')
            # 3.接受返回值，file_id
            # 4. 存储file_id 到mysql 直接return 搞定 ，运维操作一个模型类，imgeFiled的字段中会自动存储路径
            return file_id
        else:
            raise Exception('上传fdfs失败')  # 开发工具类抛出异常，不能捕获异常，让运维知道哪里出错

    def exists(self, name):
        """文件存在返回True 反之返回False"""
        return False  # 告诉django文件不存在系统当中,文件都存到FastDFS里面去了 True 就不会调用_save()

    # 上面都是存储，这里是下载
    def url(self, name):
        """可以返回要下载的文件的全路径,提供给用户下载时使用.
           name 就是要下载的文件的名字, 将来会用数据库中的file_id传到url，
           这里需要拼接完整路径
           ｒｅｔｕｒｎ  http://192.168.247.128:8888/group1/M00/00/00/wKj3gFqVBmeAeWoFAABzHhdyL04196.png
           sku.image.url
        """
        return self.server_ip + name # 自己拼接地址
