IMAGE_ubuntu_2204   = "bento/ubuntu-24.04"
IMAGE_Debian_12     = "bento/debian-12"

ENV['VAGRANT_NO_PARALLEL'] = 'yes'

Vagrant.configure(2) do |config|

  config.vm.provision "shell", inline: <<-SHELL
    sudo useradd -m -s /bin/bash nima || true
    echo "nima:nima" | sudo chpasswd    # Add user `nima` with password `nima`
    echo "nima ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/nima
  SHELL
  # config.disksize.size = '50GB'

  Nodes1 = 0
  (1..Nodes1).each do |gitlab|
    config.vm.define "gitlab-server-#{gitlab}" do |gitlab_vm|
      gitlab_vm.vm.box = IMAGE_Debian_12
      gitlab_vm.vm.hostname = "gitlab-server-#{gitlab}.domain.local"
      gitlab_vm.vm.network "private_network", ip: "192.168.56.1#{gitlab}"
      gitlab_vm.vm.network "forwarded_port", guest: 22, host: 2211, id: "ssh"
      gitlab_vm.vm.provider "virtualbox" do |v|
        v.name = "gitlab-server-#{gitlab}"
        v.memory = 8196
        v.cpus = 4
        # v.disksize.size = '50GB'
        # v.customize ["modifyhd", "#{Dir.pwd}/.vagrant/machines/default/virtualbox/disk.vmdk", "--resize", 50000]
      end
    end
  end

  Nodes2 = 0
  (1..Nodes2).each do |docker|
    config.vm.define "docker-server-#{docker}" do |docker_vm|
      docker_vm.vm.box = IMAGE_Debian_12
      docker_vm.vm.hostname = "docker-server-#{docker}.domain.local"
      docker_vm.vm.network "private_network", ip: "192.168.56.3#{docker}"
      docker_vm.vm.network "forwarded_port", guest: 22, host: 2231, id: "ssh"
      docker_vm.vm.provider "virtualbox" do |v|
        v.name = "docker-server-#{docker}"
        v.memory = 1024
        v.cpus = 1
      end
    end
  end


  Nodes3 = 0
  (1..Nodes3).each do |nginx|
    config.vm.define "nginx-server-#{nginx}" do |nginx_vm|
      nginx_vm.vm.box = IMAGE_Debian_12
      nginx_vm.vm.hostname = "nginx-server-#{nginx}.domain.local"
      nginx_vm.vm.network "private_network", ip: "192.168.56.5#{nginx}"
      nginx_vm.vm.network "forwarded_port", guest: 22, host: 2251, id: "ssh"
      nginx_vm.vm.provider "virtualbox" do |v|
        v.name = "nginx-server-#{nginx}"
        v.memory = 1024
        v.cpus = 1
      end
    end
  end


  Nodes4 = 0
  (1..Nodes4).each do |wordpress|
    config.vm.define "wordpress-server-#{wordpress}" do |wordpress_vm|
      wordpress_vm.vm.box = IMAGE_Debian_12
      wordpress_vm.vm.hostname = "wordpress-server-#{wordpress}.domain.local"
      wordpress_vm.vm.network "private_network", ip: "192.168.56.7#{wordpress}"
      wordpress_vm.vm.network "forwarded_port", guest: 22, host: 2271, id: "ssh"
      wordpress_vm.vm.provider "virtualbox" do |v|
        v.name = "wordpress-server-#{wordpress}"
        v.memory = 1024
        v.cpus = 1
      end
    end
  end

    Nodes5 = 1
  (1..Nodes5).each do |wordpress|
    config.vm.define "asma-wp-test" do |asma_wp_test|
      asma_wp_test.vm.box = IMAGE_ubuntu_2204
      asma_wp_test.vm.hostname = "asma-wp-test.nima.local"
      asma_wp_test.vm.network "private_network", ip: "192.168.252.100"
      asma_wp_test.vm.network "forwarded_port", guest: 22, host: 8090, id: "ssh"
      asma_wp_test.vm.provider "virtualbox" do |v|
        v.name = "Asma-WP-Test-1"
        v.memory = 4096
        v.cpus = 2
      end
    end
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbooks/defaults.yml"
    ansible.inventory_path = "inventories/lab/hosts.yml"
  end

end
