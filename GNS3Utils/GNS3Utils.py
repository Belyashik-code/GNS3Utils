import json
from typing import Union, Dict, List, Any
from requests import Session
from json import dumps
import time


class GNS3Utils:

    def __init__(self, server: str, port: Union[int, str], gns3_api_version: str = "v3"):
        self.server = server
        self.port = port
        self.gns3_api_version = gns3_api_version
        self.__link = f"{self.server}:{self.port}"

        self.projects = self.__Projects(self)
        self.users = self.__Users(self)
        self.nodes = self.__Nodes(self)
        self.links = self.__Links(self)
        self.computes = self.__Computes(self)

        self.session = Session()
        self.session.headers.update({"Authorization": f'Bearer {self.users.get_auth_token()}'})


    class __Users:

        def __init__(self, outer_inst):
            self.outer_inst = outer_inst

        def get_auth_token(self, username: str = "admin", password: str = "admin"):
            url = f"{self.outer_inst.get_base_url()}/access/users/authenticate"
            data = dumps({"username": username, "password": password})
            response = self.outer_inst.session.post(url, data=data)
            return response.json()["access_token"]


    class __Projects:

        def __init__(self, outer_inst):
            self.outer_inst = outer_inst

        def open_project(self, project_id: str):
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/open"
            response = self.outer_inst.session.post(url)
            return  response.json()

        def create_project(self, project_name: str) -> dict:
            url = f"{self.outer_inst.get_base_url()}/projects"
            data = dumps({"name": project_name})
            response = self.outer_inst.session.post(url, data=data)
            return response.json()

        def get_projects(self) -> dict:
            url = f"{self.outer_inst.get_base_url()}/projects"
            response = self.outer_inst.session.get(url)
            return response.json()

        def duplicate_project_by_id(self, project_id: str, name: str = None) -> dict:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/duplicate"
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
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}"
            response = self.outer_inst.session.delete(url)
            return response.status_code

        def delete_project_by_name(self, project_name: str) -> int:
            project_id = self.get_project_by_name(project_name)["project_id"]
            return self.delete_project_by_id(project_id)

        def get_project_by_name(self, name: str) -> dict:
            projects = self.get_projects()
            response = next((item for item in projects if item["name"] == name), None)
            return response

        def get_project_by_id(self, project_id: str) -> dict:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}"
            response = self.outer_inst.session.get(url)
            return response.json()


    class __Nodes:

        def __init__(self, outer_inst):
            self.outer_inst = outer_inst

        def create_node(self, node_name: str, project_id: str, node_type: str, compute_id: str = "local", console: int = None,
                        console_type: str = None, console_auto_start: bool = None, aux: int = None, aux_type: str = None,
                        properties: object = None, label: object = None, symbol: str = None, x: int = None, y: int = None, z: int = None,
                        locked: bool = None, port_name_format: str = None, port_segment_size: int = None, first_port_name: str = None,
                        custom_adapters: list[object] = None) -> dict:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/nodes"
            data = {"name": node_name, "node_type": node_type, "compute_id": compute_id}
            data.update({"console": console})  if console is not None else None
            data.update({"console_type": console_type}) if console_type is not None else None
            data.update({"console_auto_start": console_auto_start}) if console_auto_start is not None else None
            data.update({"aux": aux}) if aux is not None else None
            data.update({"aux_type": aux_type}) if aux_type is not None else None
            data.update({"properties": properties}) if properties is not None else None
            data.update({"label": label}) if label is not None else None
            data.update({"symbol": symbol}) if symbol is not None else None
            data.update({"x": x}) if x is not None else None
            data.update({"y": y}) if y is not None else None
            data.update({"z": z}) if z is not None else None
            data.update({"locked": locked}) if locked is not None else None
            data.update({"port_name_format": port_name_format}) if port_name_format is not None else None
            data.update({"port_segment_size": port_segment_size}) if port_segment_size is not None else None
            data.update({"first_port_name": first_port_name}) if first_port_name is not None else None
            data.update({"custom_adapters": custom_adapters}) if custom_adapters is not None else None
            response = self.outer_inst.session.post(url, data=json.dumps(data))
            return response.json()

        def get_project_nodes(self, project_id: str) -> list[dict]:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/nodes"
            response = self.outer_inst.session.get(url)
            return response.json()

        def start_project_nodes(self, project_id: str) -> int:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/nodes/start"
            response = self.outer_inst.session.post(url)
            return response.status_code

        def stop_project_nodes(self, project_id: str) -> int:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/nodes/stop"
            response = self.outer_inst.session.post(url)
            return response.status_code

        def suspend_project_nodes(self, project_id: str) -> int:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/nodes/suspend"
            response = self.outer_inst.session.post(url)
            return response.status_code

        def reload_project_nodes(self, project_id: str) -> int:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/nodes/reload"
            response = self.outer_inst.session.post(url)
            return response.status_code

        # todo make get universal method for project name/ project id
        def get_project_node_by_id(self, project_id: str, node_id: str) -> dict:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/nodes/{node_id}"
            response = self.outer_inst.session.get(url)
            return response.json()

        def get_project_node_by_name(self, project_id: str, name: str) -> dict:
            project_nodes = self.get_project_nodes(project_id)
            project_node = next((item for item in project_nodes if item["name"] == name), None)
            return project_node

        def delete_project_node_by_id(self, project_id: str, node_id: str) -> int:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/nodes/{node_id}"
            response = self.outer_inst.session.delete(url)
            return response.status_code

        def delete_project_node_by_name(self, project_id: str, name: str) -> int:
            project_nodes = self.get_project_nodes(project_id)
            project_node = next((item for item in project_nodes if item["name"] == name), None)
            return self.delete_project_node_by_id(project_id, project_node["node_id"])

        def get_project_node_links_by_id(self, project_id: str, node_id: str) -> list[dict]:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/nodes/{node_id}/links"
            response = self.outer_inst.session.get(url)
            return response.json()

        def get_project_node_links_by_name(self, project_id: str, node_name: str) -> list[dict]:
            node_id = self.get_project_node_by_name(project_id, node_name)["node_id"]
            node_links = self.get_project_node_links_by_id(project_id, node_id)
            return node_links

        def get_project_node_ports_status_by_id(self, project_id: str, node_id: str) -> dict:
            ports = self.get_project_node_by_id(project_id, node_id)["ports"]
            links = self.get_project_node_links_by_id(project_id, node_id)
            linked_adapters = []
            free_adapters = []
            for link in links:
                for node in link["nodes"]:
                    if node["node_id"] == node_id:
                        linked_adapters.append({"adapter_number": node["adapter_number"],
                                              "port_number": node["port_number"]})
            for port in ports:
                if {"adapter_number": port["adapter_number"],
                    "port_number": port["port_number"]} not in linked_adapters:
                    free_adapters.append({"adapter_number": port["adapter_number"],
                                          "port_number": port["port_number"]})
            return {"free_ports": free_adapters, "linked_ports": linked_adapters}

        def get_project_node_ports_status_by_name(self, project_id: str, node_name: str) -> dict:
            node_id = self.get_project_node_by_name(project_id, node_name)["node_id"]
            ports_status = self.get_project_node_ports_status_by_id(project_id, node_id)
            return ports_status

    class __Links:

        def __init__(self, outer_inst):
            self.outer_inst = outer_inst

        def get_project_links_by_project_id(self, project_id: str) -> list[dict]:
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/links"
            response = self.outer_inst.session.get(url)
            return response.json()

        def get_project_links_by_project_name(self, name: str) -> list[dict]:
            project_id = self.outer_inst.projects.get_project_by_name(name)["project_id"]
            project_links = self.get_project_links_by_project_id(project_id)
            return project_links

        def create_new_link_by_node_ids(self, project_id: str, first_node_id: str, second_node_id: str,
                                        first_node_ports: dict = None, second_node_ports: dict = None) -> dict:
            if first_node_ports is None and second_node_ports is None:
                first_node_free_ports = self.outer_inst.nodes.get_project_node_ports_status_by_id(project_id, first_node_id)["free_ports"]
                second_node_free_ports = self.outer_inst.nodes.get_project_node_ports_status_by_id(project_id, second_node_id)["free_ports"]
                if len(first_node_free_ports) > 0 and len(second_node_free_ports) > 0:
                    data = {"nodes": [{
                        "node_id": first_node_id,
                        "adapter_number": first_node_free_ports[0]["adapter_number"],
                        "port_number": first_node_free_ports[0]["port_number"]
                        },
                        {
                            "node_id": second_node_id,
                            "adapter_number": second_node_free_ports[0]["adapter_number"],
                            "port_number": second_node_free_ports[0]["port_number"]
                        }
                    ]}
                    print(data)
            else:
                data = {"nodes": [first_node_ports, second_node_ports]}
            url = f"{self.outer_inst.get_base_url()}/projects/{project_id}/links"
            response = self.outer_inst.session.post(url, data=json.dumps(data))
            return response.json()



    class __Computes:

        def __init__(self, outer_inst):
            self.outer_inst = outer_inst

        def get_computes(self) -> dict:
            url = f"{self.outer_inst.get_base_url()}/computes"
            response = self.outer_inst.session.get(url)
            return response.json()


    def get_base_url(self):
        return f"http://{self.__link}/{self.gns3_api_version}"
