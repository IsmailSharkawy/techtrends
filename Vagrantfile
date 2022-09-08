# set up the default terminal
ENV["TERM"]="linux"

# set minimum version for Vagrant
Vagrant.require_version ">= 2.2.10"
Vagrant.configure("2") do |config|
  config.vm.provision "shell",
    inline: "sudo su - && sudo apt -y install zypper && zypper update && zypper install -y apparmor-parser"
  
  # Set the image for the vagrant box
  config.vm.box = "centos/7"
  # Set the image version

  # Forward the ports from the guest VM to the local host machine
  # Forward more ports, as needed
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 6111, host: 6111
  config.vm.network "forwarded_port", guest: 6112, host: 6112

  # Set the static IP for the vagrant box
  config.vm.network "private_network", ip: "192.168.50.5"
  
  # Configure the parameters for VirtualBox provider
  config.vm.provider "qemu" do |qe|
    qe.arch = "x86_64"
    qe.machine = "q35"
    qe.cpu = "max"
    qe.net_device = "virtio-net-pci"
  end
end
