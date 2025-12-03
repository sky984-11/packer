source "vsphere-iso" "this" {
  vcenter_server    = var.vsphere_server
  username          = var.vsphere_user
  password          = var.vsphere_password
  datacenter        = ""
  cluster           = var.cluster
  insecure_connection  = true

  vm_name = var.vm_name
  notes = var.annotation
  guest_os_type = "debian12_64Guest"
  ssh_username = var.ssh_username
  ssh_password = var.ssh_password
  ssh_host = var.vm_ip
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
      "<esc><wait>",
      "install <wait>",
      "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg <wait>",
      "debian-installer=en_US.UTF-8 <wait>",
      "auto <wait>",
      "locale=en_US.UTF-8 <wait>",
      "kbd-chooser/method=us <wait>",
      "keyboard-configuration/xkb-keymap=us <wait>",
      "netcfg/get_ipaddress=${var.vm_ip} <wait>",
      "netcfg/get_netmask=${var.vm_netmask} <wait>",
      "netcfg/get_gateway=${var.vm_gateway} <wait>",
      "netcfg/get_nameservers=${var.vm_dns} <wait>",
      "netcfg/disable_autoconfig=true <wait>",
      "netcfg/get_hostname=${var.vm_name} <wait>",
      "netcfg/get_domain=catixs.net <wait>",
      "fb=false <wait>",
      "debconf/frontend=noninteractive <wait>",
      "console-setup/ask_detect=false <wait>",
      "console-keymaps-at/keymap=us <wait>",
      "grub-installer/bootdev=/dev/sda <wait>",
      "<enter><wait>"
  ]
}

build {
  sources  = [
    "source.vsphere-iso.this"
  ]
}
