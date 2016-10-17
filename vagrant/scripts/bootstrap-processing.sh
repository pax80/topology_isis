#!/bin/bash -x
PY_ENV_NAME='venv'
TOPOLOGY_HOME='/usr/local/topology'
TOPOLOGY_LIB='/usr/local/topology/src'

#echo "====== Installing updates and packages ====="
wget -O - http://debian.neo4j.org/neotechnology.gpg.key| apt-key add - # Import our signing key
echo 'deb http://debian.neo4j.org/repo stable/' > /etc/apt/sources.list.d/neo4j.list # Create an Apt sources.list file

echo "====== Setting up additional deian sources ====="
echo "deb http://http.debian.net/debian jessie-backports main" > /etc/apt/sources.list.d/jessie_backports.list

apt-get install -y python2.7-dev
apt-get install -y virtualenvwrapper
apt-get install -y libxml2-dev libxslt1-dev
apt-get install -y redis-server
apt-get install -y curl
apt-get install -y neo4j


echo "====== Creating user observer ====="
groupadd topology
useradd topology -d $TOPOLOGY_HOME -g topology --create-home --shell=/bin/bash
# set password to observer
echo "topology:topology" | chpasswd
usermod topology -G sudo -a  # add to sudo group



echo "====== Setting up Python ====="
grep -q PYTHONPATH $TOPOLOGY_HOME/.bashrc || echo "PYTHONPATH=$TOPOLOGY_LIB" >> $TOPOLOGY_HOME/.bashrc
grep -q 'export PYTHONPATH' $TOPOLOGY_HOME/.bashrc || echo 'export PYTHONPATH' >> $TOPOLOGY_HOME/.bashrc
cd $TOPOLOGY_HOME
su topology -c "virtualenv $PY_ENV_NAME"
PIP_PATH="$TOPOLOGY_HOME/$PY_ENV_NAME/bin/pip"
su topology -c "$PIP_PATH install -r /vagrant/requirements.txt"
su topology -c "$PIP_PATH install nose"  # required for tests running

echo "====== Create topology file structure ====="
[ -d $TOPOLOGY_HOME/etc ] || install -d -otopology -gtopology -m750 $TOPOLOGY_HOME/etc
[ -f $TOPOLOGY_HOME/etc/topology.conf ] || cp /vagrant/vagrant/etc/topology-default.conf $TOPOLOGY_HOME/etc/topology.conf
[ -d $TOPOLOGY_HOME/src ] || install -d -otopology -gtopology -m750 $TOPOLOGY_HOME/src
[ -L $TOPOLOGY_HOME/src/topology ] || ln -s /vagrant/topology $TOPOLOGY_HOME/src


[ -d $TOPOLOGY_HOME/var ] || install -d -otopology -gtopology -m750 $TOPOLOGY_HOME/var
[ -d $TOPOLOGY_HOME/var/tmp ] || install -d -otopology -gtopology -m750 $TOPOLOGY_HOME/var/tmp
[ -d $TOPOLOGY_HOME/var/xml ] || install -d -otopology -gtopology -m777 $TOPOLOGY_HOME/var/xml
[ -d $TOPOLOGY_HOME/var/error_xml ] || install -d -otopology -gtopology -m750 $TOPOLOGY_HOME/var/error_xml
[ -d /data/tmp ] || install -d -otopology -gtopology -m750 /data/tmp
[ -d /data/backup ] || install -d -otopology -gtopology -m750 /data/backup


