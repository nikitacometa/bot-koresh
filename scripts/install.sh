#!/bin/bash

sudo apt update && apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev openssl git pipenv tor || exit

git clone https://github.com/wackloner/bot-koresh.git ~/bot-koresh

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile

pyenv install 3.8.5
pyenv global 3.8.5

~/.pyenv/versions/3.8.5/bin/pip3 install pipenv
~/.pyenv/versions/3.8.5/bin/pipenv install

pipenv install --dev

# Mongo
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt update && install -y mongodb-org

sudo cp ~/bot-koresh/koresh.service /etc/systemd/system
sudo systemctl daemon-reload
