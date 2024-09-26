import json
from typing import Union
from requests import Session
from json import dumps
import time


class GNS3APIManager:

    def __init__(self, server: str, port: Union[int, str], gns3_api_version: str = "v3"):
        self.server = server
        self.port = port
        self.gns3_api_version = gns3_api_version
        self.link = f"{self.server}:{self.port}"

        self.projects = self.__Projects(self)
        self.auth = self.__Auth(self)

        self.session = Session()
        self.session.headers.update({"Authorization": f'Bearer {self.auth.get_auth_token()}'})

    class __Auth:

        def __init__(self, outer_inst):
            self.outer_inst = outer_inst

        def get_auth_token(self, username: str = "admin", password: str = "admin"):
            url = f"http://{self.outer_inst.link}/{self.outer_inst.gns3_api_version}/access/users/authenticate"
            data = dumps({"username": username, "password": password})
            response = self.outer_inst.session.post(url, data=data)
            return response.json()["access_token"]

    class __Projects:

        def __init__(self, outer_inst):
            self.outer_inst = outer_inst


        def open_project(self, project_id: str):
            url = f"http://{self.outer_inst.link}/{self.outer_inst.gns3_api_version}/projects/{project_id}/open"
            response = self.outer_inst.session.post(url)
            return  response.json()

        def create_project(self, project_name: str) -> dict:
            url = f"http://{self.outer_inst.link}/{self.outer_inst.gns3_api_version}/projects"
            data = dumps({"name": project_name})
            response = self.outer_inst.session.post(url, data=data)
            return response.json()

        def duplicate_project_by_id(self, project_id: str, name: str = None) -> dict:
            url = f"http://{self.outer_inst.link}/{self.outer_inst.gns3_api_version}/projects/{project_id}/duplicate"
            data = self.get_project_by_id(project_id)
            data.update({"name": name if name is not None else f"{data['name']}_clone{time.time():.0f}"})
            response = self.outer_inst.session.post(url, data=json.dumps(data))
            return response.json()

        def duplicate_project_by_name(self, project_name: str, new_name: str = None) -> dict:
            project_id = self.get_project_by_name(project_name)["project_id"]
            if project_id is not None:
                return self.duplicate_project_by_id(project_id, new_name)
            else:
                return {}

        def delete_project_by_id(self, project_id: str) -> int:
            url = f"http://{self.outer_inst.link}/{self.outer_inst.gns3_api_version}/projects/{project_id}"
            response = self.outer_inst.session.delete(url)
            return response.status_code

        def delete_project_by_name(self, project_name: str) -> int:
            project_id = self.get_project_by_name(project_name)["project_id"]
            if project_id is not None:
                return self.delete_project_by_id(project_id)
            else:
                return 0

        def get_project_by_name(self, name) -> dict:
            url = f"http://{self.outer_inst.link}/{self.outer_inst.gns3_api_version}/projects"
            response = self.outer_inst.session.get(url)
            project = next((item for item in response.json() if item["name"] == name), None)
            return project

        def get_project_by_id(self, project_id: str) -> dict:
            url = f"http://{self.outer_inst.link}/{self.outer_inst.gns3_api_version}/projects/{project_id}"
            response = self.outer_inst.session.get(url)
            return response.json()

    #
    # def getProjectById(self, project_id, server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port']):
    #     url = f"http://{server_ip}:{server_port}/v2/projects"
    #     response = get(url)
    #     if response.status_code == 200:
    #         project = next((item for item in response.json() if item["project_id"] == project_id), None)
    #         return project
    #     else:
    #         return False
    #
    # def getProjectNodeIdByName(self, node_name, server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port'],
    #                            project_id= config.gns3_server['autotest_project_id']):
    #     url = f"http://{server_ip}:{server_port}/v2/projects/{project_id}/nodes"
    #     response = get(url)
    #     if response.status_code == 200:
    #         project = next((item for item in response.json() if item["name"] == node_name), None)
    #         return project
    #     else:
    #         return False
    #
    # def deleteTemplates(id, server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port']):
    #     url = f"http://{server_ip}:{server_port}/v2/templates/{id}"
    #     print(url)
    #     response = delete(url)
    #     print(response)
    #
    #
    # def postTemplate(json_file, server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port']):
    #     url = f"http://{server_ip}:{server_port}/v2/templates"
    #     data = dumps(json_file)
    #     response = post(url, data=data)
    #     print(response.json())
    #     if response.status_code == 200:
    #         print(response)
    #     else:
    #         print(response.status_code)
    #
    # def postProjectNodes(node_json, server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port'],
    #                      project_id= config.gns3_server['autotest_project_id']):
    #
    #     url = f"http://{server_ip}:{server_port}/v2/projects/{project_id}/nodes"
    #     data = dumps(node_json)
    #     response = post(url, data=data)
    #     print(response.json())
    #
    #
    # def postProjectLinks(link_json , server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port'],
    #                      project_id= config.gns3_server['autotest_project_id']):
    #     url = f"http://{server_ip}:{server_port}/v2/projects/{project_id}/links"
    #     # /-/-/-/-/-/-/-/-/-/-/-/-/-/-/
    #     # convert node name to node id
    #     # выполняем преобразование имени ноды в id
    #     link_json['nodes'][0]['node_id'] = getProjectNodeIdByName(link_json['nodes'][0]['node_id'], project_id=project_id)['node_id']
    #     link_json['nodes'][1]['node_id'] = getProjectNodeIdByName(link_json['nodes'][1]['node_id'], project_id=project_id)['node_id']
    #     # /-/-/-/-/-/-/-/-/-/-/-/-/-/-/
    #     data = dumps(link_json)
    #     print(data)
    #     response = post(url, data=data)
    #     print(response.json())
    #
    #
    # def postProjectNodesStart( server_ip=config.gns3_server['ip'], server_port=config.gns3_server['port'],
    #                            project_id= config.gns3_server['autotest_project_id']):
    #     url = f"http://{server_ip}:{server_port}/v2/projects/{project_id}/nodes/start"
    #     response = post(url)
    #     print(response)
    #     return response

