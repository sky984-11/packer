# 基于 Packer 的 ESXI 自动化部署
这是一个使用 Packer 实现 VMware ESXi 虚拟机自动化部署的项目。

## 下载packer

```sh
wget https://releases.hashicorp.com/packer/1.14.3/packer_1.14.3_linux_amd64.zip
unzip packer_1.14.3_linux_amd64.zip
mv packer /usr/local/bin/packer
```

## 插件安装

```sh
packer plugins install github.com/hashicorp/vsphere
```

## 构建ubuntu虚拟机

```sh
packer build \
  -var 'vsphere_server=10.4.10.140' \
  -var 'vsphere_user=root' \
  -var 'vsphere_password=Catixs@3202' \
  -var 'cluster=localhost' \
  -var 'datastore=HK_DATA' \
  -var 'network_name=VLAN 10' \
  -var 'ssh_username=vagrant' \
  -var 'ssh_password=vagrant' \
  -var 'iso_path=[HK_DATA] ISO/ubuntu-22.04.5-live-server-amd64.iso' \
  -var 'vm_name=tf-edu-ubuntu' \
  -var 'host_name=ubuntu-test' \
  -var 'vm_cpus=2' \
  -var 'vm_ram=2048' \
  -var 'vm_disk_size=22144' \
  -var 'ssh_password=$6$0ovtYUWS7QOv0tPi$E/vBi.DcAvKrheYl/3K0w/.ZlzD1MM6PGHa89c2jv7qA1pV//abEHMdpDfC1E27pFJ10t6cBt0Bt7Y9s7bwCO/' \
  ./builds/ubuntu/22.04
```

## 注意事项
1. packer构建的http网络esxi必须可以访问