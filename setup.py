from setuptools import setup, find_packages
import subprocess

gns3_tag_version = subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='GNS3Utils',
  version=gns3_tag_version,
  author='Beliaev Aleksandr',
  author_email='belyaevaleksandr@icloud.com',
  description='This project can help you with GNS3 automation',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Belyashik-code/GNS3Utils',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='gns3 GNS3 GNS3API',
  project_urls={
    'Documentation': 'https://github.com/Belyashik-code/GNS3Utils'
  },
  python_requires='>=3.7'
)