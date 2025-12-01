source "vsphere-iso" "this" {
  vcenter_server    = var.vsphere_server
  username          = var.vsphere_user
  password          = var.vsphere_password
  datacenter        = ""
  cluster           = var.cluster
  insecure_connection  = true

  vm_name = var.vm_name
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
  http_directory = "http/ubuntu/22.04"
  boot_wait = "5s"

  boot_command = [
  "c",
  "linux /casper/vmlinuz --- autoinstall quiet 'ds=nocloud-net;s=http://{{ .HTTPIP }}:{{ .HTTPPort }}/' ip=45.67.201.205::45.67.201.193:255.255.255.240:tf-edu-ubuntu:ens192:none nameserver=8.8.8.8",
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
