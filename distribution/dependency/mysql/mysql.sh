# 拉取docker镜像:
docker pull mysql:5.7

# 准备文件夹
rm -rf /data/tristan/mysql/data
mkdir -p /data/tristan/mysql/data

#准备binlog
# 上传mysql.cnf到服务器
mv -f mysql.cnf /data/tristan/mysql/mysql.cnf

# 运行docker:
docker stop mymysql
docker rm   mymysql

docker run --name  mymysql -p 3306:3306 --restart=always --privileged=true \
    -v /etc/localtime:/etc/localtime:ro \
    -v /data/tristan/mysql/mysql.cnf:/etc/mysql/conf.d/mysql.cnf \
    -v /data/tristan/mysql/data:/var/lib/mysql \
    -e TZ=Asia/Shanghai \
    -e MYSQL_ROOT_PASSWORD=tristan123 \
    -e MYSQL_DATABASE=laashub \
    -e MYSQL_USER=laashub \
    -e MYSQL_PASSWORD=laashub123 \
    -d mysql:5.7  \
    --character-set-server=utf8mb4  \
    --collation-server=utf8mb4_unicode_ci

# 查看日志
docker logs -f mymysql

# 外部无法访问?

# 进入容器内部:
docker exec -it mymysql /bin/bash

# 连接mysql
mysql -uroot -p
# 输入: tristan123

# 修改访问设置
ALTER USER 'laashub'@'%' IDENTIFIED WITH mysql_native_password BY 'laashub123';

# 刷新权限
FLUSH PRIVILEGES;