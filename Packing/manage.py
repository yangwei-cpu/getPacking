#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# 一个实用的命令行工具，可让你以各种方式与该 Django 项目进行交互。
"""
启动方式：执行命令：python3 manage.py runserver 0.0.0.0:8000
如果端口被占用清除端口：lsof -i:8000   kill -9 XXX
访问路径：http://127.0.0.1:8000/runoob/
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Packing.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
