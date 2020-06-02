mkdir -p /data/tristan/laashub/nginx/ca
mv default.conf /data/tristan/laashub/nginx/
mv 3654329_preview.laashub.com_nginx.zip /data/tristan/laashub/nginx/ca/
yum install -y unzip
cd /data/tristan/laashub/nginx/ca/ &&
unzip /data/tristan/laashub/nginx/ca/3654329_preview.laashub.com_nginx.zip -d /data/tristan/laashub/nginx/ca
ls -al /data/tristan/laashub/nginx/ca/

docker stop mynginx
docker rm   mynginx

docker run -d --restart=always --name mynginx -p 80:80 -p 443:443 -v /data/tristan/laashub/nginx/default.conf:/etc/nginx/conf.d/default.conf -v /data/tristan/laashub/nginx/ca:/etc/nginx/ca nginx

docker logs -f --tail 100 mynginx