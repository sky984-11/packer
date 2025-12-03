source "vsphere-iso" "this" {
  vcenter_server    = var.vsphere_server
  username          = var.vsphere_user
  password          = var.vsphere_password
  datacenter        = ""
  cluster           = var.cluster
  insecure_connection  = true

  vm_name = var.vm_name
  notes = var.annotation
  guest_os_type = "ubuntu64Guest"
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
    "c",
    "linux /casper/vmlinuz --- autoinstall quiet 'ds=nocloud-net;s=http://{{ .HTTPIP }}:{{ .HTTPPort }}/' ip=${var.vm_ip}::${var.vm_gateway}:${var.vm_netmask}:${var.host_name}:ens192:none",
    "<enter>",
    "initrd /casper/initrd",
    "<enter>",
    "boot",
    "<enter>"
]
}

build {
  sources  = [
    "source.vsphere-iso.this"
  ]
}
