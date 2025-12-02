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
  http_directory = "http/debian/12"
  boot_wait = "5s"
  # 这里使用静态IP，如果dhcp则去掉ip后面的一串内容
  boot_command = [
        "<esc><wait>",
        "<esc><wait>",
        "<enter><wait>",
        "/install/vmlinuz<wait>",
        " initrd=/install/initrd.gz",
        " auto-install/enable=true",
        " debconf/priority=critical",
        " preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg<wait>",
        " -- <wait>",
        "<enter><wait>"
]
}

build {
  sources  = [
    "source.vsphere-iso.this"
  ]
}
