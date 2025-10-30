import os
from setuptools import setup, find_packages

# 获取 setup.py 所在目录
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='piper_sdk',
    version='0.6.1',
    setup_requires=['setuptools>=40.0'],
    long_description=open(os.path.join(here, 'DESCRIPTION.MD'), encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/agilexrobotics/piper_sdk',
    license='MIT License',
    packages=find_packages(include=['piper_sdk', 'piper_sdk.*']),
    include_package_data=True,
    package_data={
        '': ['LICENSE', '*.sh', '*.MD'],
        'piper_sdk/asserts': ['*'],
    },
    install_requires=[
        'python-can>=3.3.4',
    ],
    entry_points={},
    author='Agilex Robotice Co., Ltd.',
    author_email='',
    description='A sdk to control Agilex piper arm',
    platforms=['Linux'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    project_urls={
        'Repository': 'https://github.com/agilexrobotics/piper_sdk',
        'ChangeLog': 'https://github.com/agilexrobotics/piper_sdk/blob/master/CHANGELOG.MD',
    },
)
