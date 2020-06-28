from django.conf import settings
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client


class FastDFSStorage(Storage):
    """
    自定义文件存储方案：将文件转存到FastDFS
    """

    def __init__(self, base_url=None, client_conf=None):
        """
        初始化
        :param base_url: 用于构造图片完整路径使用，图片服务器的域名
        :param client_conf: FastDFS客户端配置文件的路径
        """
        # if base_url is None:
        #     base_url = settings.FDFS_URL
        self.base_url = base_url or settings.FDFS_BASE_URL
        # if client_conf is None:
        #     client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf or settings.FDFS_CLIENT_CONF

    def _open(self, name, mode='rb'):
        """打开文件时候被调用，此业务逻辑不涉及文件打开，此方法无实际用处，
        但是官方文档中规定必须提供此方法，所以直接pass
        """
        pass

    def _save(self, name, content):
        """
        保存文件时被调用
        就是在这个方法被调用时，将发送给django的文件存储到fastdfs
        :param name: 要保存的文件的名字
        :param content: 要保存的文件的对象，file类型，通过read()方法读取对象中文件内容的二进制
        :return:
        """
        # 创建client对象
        client = Fdfs_client(self.client_conf)
        # 调用上传的方法：upload_by_buffer('文件的二进制')  利用要保存文件的二进制上传到fastdfs
        ret = client.upload_by_buffer(content.read())

        """
        >>> from fdfs_client.client import Fdfs_client
        >>> client = Fdfs_client('meiduo_mall/utils/fastdfs/client.conf')
        >>> ret = client.upload_by_filename('/home/python/Desktop/01.jpeg')
        >>> ret
        {'Uploaded size': '46.00KB', 'Group name': 'group1',
            'Remote file_id': 'group1/M00/00/00/wKgggFtajw2Abtv3AAC4j90Tziw69.jpeg',
            'Storage IP': '192.168.32.128', 'Status': 'Upload successed.',
            'Local file name': '/home/python/Desktop/01.jpeg'
        }
        >>>

        """

        # 判断是否上传成功
        if ret.get('Status') !='Upload successed.':
            raise Exception('Fastdfs upload error')

        # 读取file_id
        file_id = ret.get('Remote file_id')
        # 返回file_id
        # _save()的返回值，会自动存储到ImageField字段对应的模型类属性种，并自动同步到数据库
        return file_id

    def exists(self, name):
        """
        判断文件是否存在，FastDFS可以自行解决文件的重名问题
        所以此处返回False，告诉Django上传的都是新文件
        :param name:  文件名
        :return: False
        """
        return False

    def url(self, name):
        """
        返回文件的完整URL路径
        :param name: 数据库中保存的文件名
        :return: 完整的URL
        """
        return self.base_url + name



