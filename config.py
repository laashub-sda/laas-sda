import os

import yaml

import config

project_root_path = os.getcwd()
app_conf = None
if not app_conf:
    app_conf = {}
    with open(os.path.join(project_root_path, "configs", "application.yml")) as f:
        config.app_conf = yaml.safe_load(f.read())
