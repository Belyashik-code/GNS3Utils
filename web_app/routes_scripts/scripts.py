from main import path_root
import scripts_pool
import re

def generateProject(file):
    try:
        file.save(f'{path_root}/{file.filename}')
        build_name = scripts_pool.unzip_archive(f'{path_root}/{file.filename}')
        if build_name:
            if scripts_pool.copy_build_to_gns3_server(build_name):
                scripts_pool.edit_current_config(re.search(r'(?<=/)[^/]+$', build_name)[0])
                scripts_pool.gen_project_nodes()
                scripts_pool.delete_local_files([f'{path_root}/{file.filename}', build_name])
    except Exception as err:
        print(f'Some Error: {err}')



