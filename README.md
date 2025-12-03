# 基于 Packer 的 ESXI 自动化部署
这是一个使用 Packer 实现 VMware ESXi 虚拟机自动化部署的项目。
支持debian12和ubuntu22.04系统自动化安装(其他系统慢慢增加中......)

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

## 运行
```sh
# 运行前在main.py中配置好参数
python3 main.py
```

## 注意事项
1. packer构建的http网络esxi必须可以访问