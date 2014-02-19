# -*- mode: ruby -*-
# vi: set ft=ruby :

# provision a vanilla ubuntu box

VAGRANTFILE_API_VERSION = "2"
BOX_NAME = "ubuntu"
BOX_URI = "http://files.vagrantup.com/precise64.box"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = BOX_NAME
  config.vm.box_url = BOX_URI
  config.vm.provision "docker"
end
