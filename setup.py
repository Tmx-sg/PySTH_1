# -*- coding: gbk -*-

from setuptools import setup, find_packages

setup(
    name='PySTH',  # ��Ŀ����
    version='1.0',  # ��Ŀ�汾
    author='Tao',  # ��������
    author_email='1713050146@qq.com',  # ��������
    description='A brief description of your project.',  # ��Ŀ����
    long_description=open('README.md', encoding='gbk').read(),  # �� README �ļ��ж�ȡ��ϸ����

    long_description_content_type='text/markdown',  # ������������
    url='https://github.com/Tmx-sg/PySTH_1',  # ��Ŀ����
    packages=find_packages(),  # �Զ����������Ӱ�
    py_modules=['main','load'],  # �ֶ�ָ��ģ��
    include_package_data=True,  # ����MANIFEST.in��ָ���������ļ�


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
            'python-xlib >=0.31'  # Linuxר������ʾ��
        ]
    },
    entry_points={  # ���������й���
        'console_scripts': [
            'PySTH=main:main',  # ��ں���
        ],
    },
    # classifiers=[  # �������������û��� PyPI ���ҵ������Ŀ
    #     'Programming Language :: Python :: 3',
    #     'License :: OSI Approved :: MIT License',
    #     'Operating System :: OS Independent',
    # ],
    python_requires='>=3.6',  # Python �汾Ҫ��
)
