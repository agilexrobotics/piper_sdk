import os
from setuptools import setup, find_packages

# 获取 setup.py 所在目录
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='piper_sdk',
    version='1.0.0',
    setup_requires=['setuptools>=39.0'],
    long_description=open(os.path.join(here, 'DESCRIPTION.MD'), encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/agilexrobotics/piper_sdk',
    license='MIT License',
    packages=find_packages(include=['piper_sdk', 'piper_sdk.*']),
    include_package_data=True,
    package_data={
        '': ['LICENSE', '*.sh', '*.MD'],
    },
    data_files=[
        ('share/bash-completion/completions', ['completion/piper-can']),
    ],
    install_requires=[
        'python-can>=3.3.4',
        'typing_extensions>=3.7.4,<4.2.0; python_version < "3.7"',
        'typing_extensions>=3.7.4; python_version >= "3.7"',
    ],
    entry_points={
        'console_scripts': [
            'piper-can=piper_sdk.cli.can:main',
        ],
    },
    author='Agilex Robotics Co., Ltd.',
    author_email='',
    description='A sdk to control Agilex piper arm',
    platforms=['Linux'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
    project_urls={
        'Repository': 'https://github.com/agilexrobotics/piper_sdk',
        'ChangeLog': 'https://github.com/agilexrobotics/piper_sdk/blob/master/CHANGELOG.MD',
    },
)
