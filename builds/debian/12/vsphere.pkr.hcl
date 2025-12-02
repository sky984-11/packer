source "vsphere-iso" "this" {
  vcenter_server    = var.vsphere_server
  username          = var.vsphere_user
  password          = var.vsphere_password
  datacenter        = ""
  cluster           = var.cluster
  insecure_connection  = true

  vm_name = var.vm_name
  guest_os_type = "debian12_64Guest"
  ssh_username = var.ssh_username
  ssh_password = var.ssh_password
  ssh_timeout  = "20m"

  CPUs =             var.vm_cpus
  RAM =              var.vm_ram
  RAM_reserve_all = true

  disk_controller_type =  ["pvscsi"]
  datastore = var.datastore
  storage {
    disk_size =        var.vm_disk_size
    disk_thin_provisioned = true
  }

  iso_paths = ["${var.iso_path}"]

  network_adapters {
    network =  var.network_name
    network_card = "vmxnet3"
  }
  http_directory = "http/${var.os_type}/${var.os_version}"
  boot_wait = "5s"
  # 这里使用静态IP，如果dhcp则去掉ip后面的一串内容
  boot_command = [
    "<esc><wait5>",
    "install ",
    "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg ",
    "debian-installer=en_US.UTF-8 ",
    "auto ",
    "locale=en_US.UTF-8 ",
    "keyboard-configuration/modelcode=SKIP ",
    "keyboard-configuration/layoutcode=us ",
    "keyboard-configuration/variantcode= ",
    "netcfg/get_ipaddress=${var.vm_ip} ",
    "netcfg/get_netmask=${var.vm_netmask} ",
    "netcfg/get_gateway=${var.vm_gateway} ",
    "netcfg/get_nameservers=${var.vm_dns} ",
    "netcfg/disable_autoconfig=true ",
    "netcfg/get_hostname=${var.host_name} ",
    "netcfg/get_domain=catixs.net ",
    "fb=false ",
    "debconf/frontend=noninteractive ",
    "console-setup/ask_detect=false ",
    "console-keymaps-at/keymap=us ",
    "grub-installer/bootdev=/dev/sda",
    "<enter><wait>"
  ]
}

build {
  sources  = [
    "source.vsphere-iso.this"
  ]
}
