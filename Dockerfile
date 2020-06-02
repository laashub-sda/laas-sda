FROM node:12.16.1 as frontend
WORKDIR /usr/src/app
RUN rm -rf *
COPY . .
WORKDIR /usr/src/app/workstation
RUN rm -rf dist
RUN npm config set registry https://registry.npm.taobao.org --global
RUN npm config set disturl https://npm.taobao.org/dist --global
RUN npm install
RUN npm run build
FROM python:3.6
WORKDIR /usr/src/app
RUN rm -rf *
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
RUN python3 -m compileall -b .
RUN find . -name "*.py" |xargs rm -rf
RUN rm -rf workstation
COPY --from=frontend /usr/src/app/workstation/dist /usr/src/app/workstation/dist
MAINTAINER tristan "https://github.com/tristan-tsl/laasops"
VOLUME /usr/src/app/configs
VOLUME /usr/src/app/distribution/configs
VOLUME /usr/src/app/engine_logic_dir
EXPOSE 5000
CMD [ "python", "./setup.pyc" ]