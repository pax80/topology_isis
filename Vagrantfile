# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|

    config.vm.define "processing" do |processing|
      processing.vm.box = "debian/jessie64"
      processing.vm.provision :shell, path: "vagrant/scripts/bootstrap-processing.sh"
      processing.vm.hostname = "processing"
      processing.vm.box_version = "8.2.0"
      processing.vm.box_check_update = false

    config.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "4096"]
      vb.customize ["modifyvm", :id, "--cpus", "2"]
    end

    processing.vm.network "private_network", ip: "192.168.0.9", virtualbox__intnet: "internal_net"
  end
end
