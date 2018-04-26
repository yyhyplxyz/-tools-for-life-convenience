import logging

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import ThrottledDTPHandler, FTPHandler
from pyftpdlib.servers import FTPServer
from config_ftp import *


def init_ftp_server():
    authorizer = DummyAuthorizer()
    if enable_anonymous:
        authorizer.add_anonymous(anonymous_path)

    for user in user_list:
        name,passwd,permit,homedir= user
        try:
            authorizer.add_user(name, passwd, homedir, perm=permit)
        except:
            print("配置文件错误请检查是否正确匹配了相应的用户名、密码、权限、路径")
            print(user)

    dtp_handler = ThrottledDTPHandler

    dtp_handler.read_limit = max_download
    dtp_handler.write_limit = max_upload

    handler = FTPHandler
    handler.authorizer = authorizer

    if enable_logging:
        logging.basicConfig(filename='pyftp.log', level=logging.INFO)

    handler.banner = welcom_banner
    handler.masquerade_address = masquerade_address
    handler.passive_ports = range(passive_ports[0], passive_ports[1])

    address = (ip, port)
    server = FTPServer(address, handler)
    server.max_cons = max_cons
    server.max_cons_per_ip = max_pre_ip

    server.serve_forever()


def ignor_octothrpe(text):
    for x, item in enumerate(text):
        if item == "#":
            return text[:x]
        pass
    return text


def init_user_config():
    f = open("baseftp.ini",encoding='utf-8')
    while 1:
        line = f.readline()
        if len(ignor_octothrpe(line)) > 3:
            user_list.append(line.split())
            # todo
        if not line:
            break


if __name__ == '__main__':
    user_list = []
    init_user_config()
    init_ftp_server()
