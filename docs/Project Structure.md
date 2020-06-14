# 整体层

configs: 最外层web容器的配置文件

dependency: 项目运行的脚本文件

docs: 文档

engine_logic_dir

`__init__.py`: 最外层web容器的初始化文件

config.py: 最外层web容器的配置文件

Dockerfile: 构建Docker镜像描述文件

requirements.txt: python项目依赖库清单列表

setup.py: 项目启动文件

## distribution: 分发库

dependency: 分发库运行所需要的依赖

configs: 分发库的配置文件

## engine: 引擎

localization: 本地化, 存储从分发库拉取的文件

## workstation: 工作站

src: 源码

package.json: nodejs项目依赖库清单描述文件