# GNS3Utils #

GNS3Utils is a Python package that provides a convenient interface to interact with the GNS3 server API. It allows users to manage projects, nodes, links, and computes easily.

## Installation

You can install the package via pip:

```bash
pip3 install GNS3Utils
```

----------
## Usage
Here's a quick example to get you started:

```python
from GNS3Utils import GNS3Utils

gns3 = GNS3Utils('192.168.1.1', 80)



project = gns3.projects.create_project(project_name="Some_Project")
node = gns3.nodes.create_node("test", project['project_id'], "vpcs")
print(gns3.projects.get_project_by_name(name="Some_Project"))
print(gns3.nodes.get_project_nodes(project['project_id']))
gns3.nodes.start_project_nodes(project['project_id'])
gns3.nodes.stop_project_nodes(project['project_id'])
print(gns3.nodes.get_project_node_by_id(project['project_id'], node['node_id']))
```

##  **Temporarily supports only "v3" API version** 

## License
This project is licensed under the MIT License