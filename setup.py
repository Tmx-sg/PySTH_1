# -*- coding: gbk -*-

from setuptools import setup, find_packages

setup(
    name='PySTH',  # 项目名称
    version='1.0',  # 项目版本
    author='Tao',  # 作者姓名
    author_email='1713050146@qq.com',  # 作者邮箱
    description='A brief description of your project.',  # 项目描述
    long_description=open('README.md', encoding='gbk').read(),  # 从 README 文件中读取详细描述

    long_description_content_type='text/markdown',  # 长描述的类型
    url='https://github.com/Tmx-sg/PySTH_1',  # 项目链接
    packages=find_packages(),  # 自动查找所有子包
    py_modules=['main','load'],  # 手动指定模块
    include_package_data=True,  # 包含MANIFEST.in中指定的数据文件


    install_requires=[
        'numpy >=1.25.1',
        'matplotlib >=3.9.2',
        'pandas >=2.1.4',
        'xlrd >=2.0.1',
        'rich >=13.8.1',
        'tabulate >=0.9.0',
    ],
    extras_require={
        'windows': [
            'pywin32 >=306',
            'windows-curses >=2.4.1',
        ],
        'linux': [
            'python-xlib >=0.31'  # Linux专用依赖示例
        ]
    },
    entry_points={  # 配置命令行工具
        'console_scripts': [
            'PySTH=main:main',  # 入口函数
        ],
    },
    # classifiers=[  # 分类器，帮助用户在 PyPI 上找到你的项目
    #     'Programming Language :: Python :: 3',
    #     'License :: OSI Approved :: MIT License',
    #     'Operating System :: OS Independent',
    # ],
    python_requires='>=3.6',  # Python 版本要求
)
