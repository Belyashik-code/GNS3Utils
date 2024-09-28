import time

from gns3apimanagement.gns3apimanagement import GNS3APIManager

gns3 = GNS3APIManager('192.168.1.69', 80)

# gns3.projects.create_project("Test")
# gns3.projects.get_project_by_name("Test")
# new_name = gns3.projects.duplicate_project_by_name("Test")['name']
# time.sleep(5)
# gns3.projects.delete_project_by_name("Test")
# gns3.projects.delete_project_by_name(new_name)
project_id = gns3.projects.create_project("Test")['project_id']
node_id = gns3.nodes.create_node("test", project_id, "vpcs")['node_id']
# print(gns3.nodes.get_project_nodes(project_id))
# gns3.nodes.start_project_nodes(project_id)
# gns3.nodes.stop_project_nodes(project_id)
# gns3.nodes.start_project_nodes(project_id)
# gns3.nodes.suspend_project_nodes(project_id)
print(gns3.nodes.get_project_node_by_id(project_id, node_id))
