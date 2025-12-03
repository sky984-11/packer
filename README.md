# 🚀 基于 Packer 的 ESXi 自动化部署方案

本项目通过 Packer + VMware ESXi 实现虚拟机的全自动化构建，当前已在 ESXi 8.0 上测试通过。
目前支持以下 Linux 发行版的无人值守安装：
  ·Debian 12
  ·DUbuntu 22.04 LTS
  （更多系统陆续适配中…）

## 📦 项目获取

```sh
git clone https://github.com/sky984-11/packer.git
cd packer
```

## 🔧 安装 Packer

```sh
wget https://releases.hashicorp.com/packer/1.14.3/packer_1.14.3_linux_amd64.zip
unzip packer_1.14.3_linux_amd64.zip
mv packer /usr/local/bin/packer
```

## 🧩 安装必要插件

```sh
packer plugins install github.com/hashicorp/vsphere
```

## ▶️ 运行构建

*运行前请先在 main.py 中配置相关参数（如 ESXi 主机、模板信息、IP 配置等）：*
```sh
python3 main.py
```

## ⚠️ 注意事项

1. Packer 构建阶段会启动临时 HTTP 服务，用于提供自动安装文件，因此 ESXi 必须能访问此 HTTP 服务。
2. 请确保防火墙、安全组等网络策略放行 Packer 部署链路。


## ✅ 特性优势

· 支持静态 IP 自动配置（构建完成即可直接使用）
· 支持 Ubuntu/Debian 全自动无人值守安装
· 部署参数可自定义（CPU、内存、磁盘等）
· 一条命令完成部署，快速稳定

## 📸 部署效果截图

<img width="665" height="535" alt="image" src="https://github.com/user-attachments/assets/fedb3e7f-dc4c-4ea3-9e36-6925aacc1f24" />
