#!/usr/bin/python
# -*- coding:utf-8 -*-

environments = {
    "develop": {
        "hosts": ["user@ip:22"],
        "passwords": {"user@ip:22": "password"},
        "colorize_errors": True,
        "project_name": "project_name",
        "local_path": "../",
        "remote_path": "/home/path",
        "build": "docker build -t xxxx ./nginx && docker build -t xxxx .",
        "server_up": "docker-compose up -d",
        "server_stop": "docker-compose stop",
        "server_down": "docker-compose down",
        "server_ps": "docker-compose ps",
    },
}
