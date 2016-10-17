# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|

    config.vm.define "topology" do |topology|
      topology.vm.box = "debian/jessie64"
      topology.vm.provision :shell, path: "vagrant/scripts/bootstrap-topology.sh"
      topology.vm.hostname = "topology"
      topology.vm.box_version = "8.2.0"
      topology.vm.box_check_update = false

    config.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "4096"]
      vb.customize ["modifyvm", :id, "--cpus", "2"]
    end

    topology.vm.network "private_network", ip: "192.168.0.9", virtualbox__intnet: "internal_net"
  end
end
