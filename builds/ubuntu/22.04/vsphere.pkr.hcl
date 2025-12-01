# === 动态渲染 user-data ===
locals {
  # 渲染 user-data 模板
  rendered_user_data = templatefile("${path.root}/http/ubuntu/22.04/user-data.tftpl", {
    host_name     = var.host_name
    ssh_username  = ubuntu
    ssh_password  = var.ssh_password
  })

}

# 在构建前生成 user-data 文件（覆盖原文件）
provisioner "shell-local" {
  inline = [
    # 写入渲染后的内容（注意转义换行和特殊字符）
    "cat > '${path.root}/http/ubuntu/22.04/user-data' << 'EOF'",
    local.rendered_user_data,
    "EOF"
  ]
}

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
    "linux /casper/vmlinuz --- autoinstall quiet 'ds=nocloud-net;s=http://{{ .HTTPIP }}:{{ .HTTPPort }}/'",
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
