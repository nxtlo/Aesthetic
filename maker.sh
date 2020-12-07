while true; do
    sudo apt-get install build-essential checkinstall
    sleep 1
    sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    sleep 1
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
    cd /opt
    sleep 1
    sudo wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz
    sleep 1
    sudo tar xzf Python-3.8.5.tgz
    cd Python-3.8.5
    sudo ./configure --enable-optimizations
    sleep 3
    sudo make altinstall
done