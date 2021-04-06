from requests import get, post, delete
import config
from json import dumps

def getProjectByName(name, server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port']):
    url = f"http://{server_ip}:{server_port}/v2/projects"
    response = get(url)
    if response.status_code == 200:
        project = next((item for item in response.json() if item["name"] == name), None)
        return project
    else:
        return False


def getProjectById(project_id, server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port']):
    url = f"http://{server_ip}:{server_port}/v2/projects"
    response = get(url)
    if response.status_code == 200:
        project = next((item for item in response.json() if item["project_id"] == project_id), None)
        return project
    else:
        return False

def getProjectNodeIdByName(node_name, server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port'],
                           project_id= config.gns3_server['autotest_project_id']):
    url = f"http://{server_ip}:{server_port}/v2/projects/{project_id}/nodes"
    response = get(url)
    if response.status_code == 200:
        project = next((item for item in response.json() if item["name"] == node_name), None)
        return project
    else:
        return False

def deleteTemplates(id, server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port']):
    url = f"http://{server_ip}:{server_port}/v2/templates/{id}"
    print(url)
    response = delete(url)
    print(response)


def postTemplate(json_file, server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port']):
    url = f"http://{server_ip}:{server_port}/v2/templates"
    data = dumps(json_file)
    response = post(url, data=data)
    print(response.json())
    if response.status_code == 200:
        print(response)
    else:
        print(response.status_code)

def postProjectNodes(node_json, server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port'],
                     project_id= config.gns3_server['autotest_project_id']):

    url = f"http://{server_ip}:{server_port}/v2/projects/{project_id}/nodes"
    data = dumps(node_json)
    response = post(url, data=data)
    print(response.json())


def postProjectLinks(link_json , server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port'],
                     project_id= config.gns3_server['autotest_project_id']):
    url = f"http://{server_ip}:{server_port}/v2/projects/{project_id}/links"
    # /-/-/-/-/-/-/-/-/-/-/-/-/-/-/
    # convert node name to node id
    # выполняем преобразование имени ноды в id
    link_json['nodes'][0]['node_id'] = getProjectNodeIdByName(link_json['nodes'][0]['node_id'], project_id=project_id)['node_id']
    link_json['nodes'][1]['node_id'] = getProjectNodeIdByName(link_json['nodes'][1]['node_id'], project_id=project_id)['node_id']
    # /-/-/-/-/-/-/-/-/-/-/-/-/-/-/
    data = dumps(link_json)
    print(data)
    response = post(url, data=data)
    print(response.json())


def postProjectNodesStart( server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port'],
                           project_id= config.gns3_server['autotest_project_id']):
    url = f"http://{server_ip}:{server_port}/v2/projects/{project_id}/nodes/start"
    response = post(url)
    print(response)
    return response


def postProjectOpen( server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port'],
                     project_id=config.gns3_server['autotest_project_id']):
    url = f"http://{server_ip}:{server_port}/v2/projects/{project_id}/open"
    response = post(url)
    print(response)


def postProject( server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port'],
                project_name="autobuild"):
    url = f"http://{server_ip}:{server_port}/v2/projects"
    data = dumps({"name": project_name})
    response = post(url, data=data)
    print(response.json())
    return response.json()
