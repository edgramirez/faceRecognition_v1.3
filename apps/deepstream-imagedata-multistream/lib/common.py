import os
import time
import fcntl
import struct
import socket
from os import walk


global source_type
source_type = {'IMAGE': 'image', 'RTSP': 'rtsp', 'VIDEO': 'video'}
IMAGE_GROUPS = ('blacklist', 'whitelist')

# home directory + directory to get data and store results 
DATA_AND_RESULTS = '/face_recognition_data_and_results'
HOMEDIR = os.environ['HOME'] + DATA_AND_RESULTS
SERVER_URI = 'https://mit.kairosconnect.app/'


def create_data_dir():
    path = os.environ['HOME'] +  DATA_AND_RESULTS

    try:
        os.mkdir(path)
    except FileExistsError as e:
        print("Directory {} already created".format(path))


def log_error(msg, _quit = True):
    print("-- PARAMETER ERROR --\n"*5)
    print(" %s \n" % msg)
    print("-- PARAMETER ERROR --\n"*5)
    if _quit:
        quit()
    else:
        return False


def file_exists(file_name):
    try:
        with open(file_name) as f:
            return file_name
    except OSError as e:
        return False


def file_exists_and_not_empty(file_name):
    if file_exists(file_name) and os.stat(file_name).st_size > 0:
        return True
    return False


def file_exists_and_empty(file_name):
    if file_exists(file_name) and os.stat(file_name).st_size == 0:
        return True
    return False


def read_images_in_dir(path_to_read):
    dir_name, subdir_name, file_names = next(walk(path_to_read))
    images = [item for item in file_names if '.jpeg' in item[-5:] or '.jpg' in item[-4:] or 'png' in item[-4:] ]
    return images, dir_name


def open_file(file_name, option='a+'):
    if file_exists(file_name):
        return open(file_name, option)
    return False


def get_timestamp():
    return int(time.time() * 1000)


def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
    return ':'.join('%02x' % b for b in info[18:24])


def get_ip_address(ifname):
    return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]


def get_machine_macaddresses():
    list_of_interfaces = [item for item in os.listdir('/sys/class/net/') if item != 'lo']
    macaddress_list = []
    for iface_name in list_of_interfaces:
        ip = get_ip_address(iface_name)
        if ip:
            macaddress_list.append(getHwAddr(iface_name))
            return macaddress_list


