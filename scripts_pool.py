import gns3apimanagement.gns3apimanagement as gns
import re
import shutil
import config
import os
import subprocess
import paramiko
import json
import bz2
import time

from main import path_root

def send_local(cmd: str) -> str:
    """
    # запуск команды в консоли ОС
    :param cmd: - непосредственно команда для консоли
    :param force: - это элемент "для последующего расширения" или на всякий случай. Когда мы не сможем выполнить команду
    средствами питона, мы можем её запустить исключительно в шелле , не управляемо и без вывода. Но запустим.
    :return: возвращаем вывод из консоли.
    """
    time.sleep(0.8)  # защита от спама, чтобы команды не выполнялись слишком быстро
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0 and len(result.stdout.decode()) > 0:
        return result.stdout.decode()
    return result.stderr.decode()


def install_requirements(requirements):
    """
    :param requirements: файл с необходимыми pip
    :return:
    """
    if not os.path.exists(requirements):
        raise print('File has been stolen or disappeared somewhere! (i mean requirements.txt)')

    cmd = f'pip3 install -q -r "{requirements}"'
    result = send_local(cmd)
    # error , no matching distribution found
    if 'rror' in result or 'o matching distribution found' in result or 'не найдена' in result:
        print(result)
        return False
    return True

# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/
# ftp step (scanning for last build)


def unzip_archive(archive_name):
    try:
        zipfile = bz2.BZ2File(archive_name)
        data = zipfile.read()
        new_build_archive_name = archive_name[:-4]
        open(new_build_archive_name, 'wb').write(data)
        return new_build_archive_name
    except KeyError:
        print('ERROR: Did not find in tar archive')
        return False


def copy_build_to_gns3_server(path):
    """
    :param path: local path to build
    :return: True if done , False if some ERROR
    """
    # Open a transport

    try:
        host, port = config.gns3_server['ip'], 22
        transport = paramiko.Transport((host, port))

        # Auth
        username, password = config.gns3_server['login'], config.gns3_server['password']
        transport.connect(None, username, password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        # Upload
        filename = re.search(r'(?!\/)[^\/]*\..+', path)[0]
        filepath = f"{config.gns3_server['img_path']}{filename}"
        localpath = f"{path}"
        sftp.put(localpath, filepath)

        # Close
        if sftp:
            sftp.close()
        return True

    except:
        return False
# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/
# edit configs step
def edit_current_config(buildname):
    """
    :param buildname: name of build file example="knos-disk-dev-asic-sim-0.1.0-pre-93-gd0dd1-genericx86-20201030093814.hdddirect"
    :return: it doesn`t exist
    """
    with open(f'{path_root}/projectNodesConfig.json', "r") as read_file:
        config_data = json.load(read_file)
    for json_example in config_data:
        if 'knos' in json_example['name']:
            json_example['properties']['hda_disk_image'] = buildname

    with open(f'{path_root}/projectNodesConfig.json', "w") as write_file:
        write_file.write(json.dumps(config_data, indent='\t'))
# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/
# gns3 project generation step


def gen_project_nodes():
    current_project_id = check_project_exist()
    if current_project_id:
        gns.postProjectOpen()
        with open(f'{path_root}/projectNodesConfig.json', "r") as read_file:
            json_data = json.load(read_file)
        for node_json in json_data:
            gns.postProjectNodes(node_json, project_id=current_project_id)

        with open(f'{path_root}/projectLinksConfig.json', "r") as read_file:
            json_data = json.load(read_file)
        for link_json in json_data:
            gns.postProjectLinks(link_json, project_id=current_project_id)
            gns.postProjectNodesStart(project_id=current_project_id)
    # /-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # /-/-/-/-/-/-/-/-/-/-/-/-/-/-/
    # ending step


def check_project_exist():
    project_id = gns.getProjectByName(config.gns3_server['autotest_project_name'])
    if project_id:
        setParam('autotest_project_id', f"{project_id['project_id']}")
        return project_id['project_id']
    else:
        project_id = gns.postProject(project_name='autobuild')
        setParam('autotest_project_id', f"{project_id['project_id']}")
        return project_id['project_id']


def setParam(param, value):
    with open(f'{path_root}/config.py', 'r') as config_file:
        conf = config_file.read()
    with open(f'{path_root}/config.py', 'w') as config_file:
        conf = re.sub(r'(?<=\'autotest_project_id\': \').+(?=\',)', value, conf)
        config_file.write(conf)


def delete_local_files(archive_name):
    for e in archive_name:
        if archive_name is not None:
            os.remove(e)
    # /-/-/-/-/-/-/-/-/-/-/-/-/-/-/

