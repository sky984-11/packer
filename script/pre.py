from passlib.hash import sha512_crypt
import ipaddress
import textwrap
import os

def encrypt_password(password: str) -> str:
    """生成 SHA512 密码"""
    return sha512_crypt.hash(password)

def generate_file(
    hostname: str, ip: str, gateway: str, netmask: str, dns: str,
    user: str, password: str, iso_type: str, output_dir: str = "http"
):
    """在本地项目目录生成自动化安装配置文件"""
    hashed_pw = password
    
    # 确保输出目录存在
    target_dir = os.path.join(output_dir, f'{iso_type}')
    os.makedirs(target_dir, exist_ok=True)
    
    if iso_type == "ubuntu":
        cidr = ipaddress.IPv4Network(f"0.0.0.0/{netmask}").prefixlen
        
        user_data = textwrap.dedent(f"""
        #cloud-config
        autoinstall:
          version: 1
          locale: en_US.UTF-8
          keyboard:
            layout: us
          timezone: Asia/Hong_Kong
          ssh:
            install-server: true
            allow-pw: true
          packages:
            - qemu-guest-agent
          storage:
            layout:
              name: direct
            swap:
              size: 0
          network:
            version: 2
            ethernets:
              ens192:
                dhcp4: false
                addresses: [{ip}/{cidr}]
                routes:
                  - to: default
                    via: {gateway}
                nameservers:
                  addresses: [{dns}]
          users:
            - default
            - name: ubuntu
              lock_passwd: false
              passwd: {encrypt_password(hashed_pw)}
          write_files:
            - path: /etc/ssh/sshd_config
              content: |
                PermitRootLogin yes
          identity:
            hostname: {hostname}
            username: ubuntu
            password: {encrypt_password(hashed_pw)}
        """).strip()

        # 写入本地文件
        user_data_path = os.path.join(target_dir + '/22.04', "user-data")
        meta_data_path = os.path.join(target_dir + '/22.04', "meta-data")

        with open(user_data_path, "w") as f:
            f.write(user_data)
            
        with open(meta_data_path, "w") as f:
            f.write(f"instance-id: iid-{hostname}\nlocal-hostname: {hostname}")
            
        print(f"✅ [本地] 已生成 Ubuntu autoinstall 配置到 {target_dir}/")

    elif iso_type == "debian":
        preseed = textwrap.dedent(f"""
            ### --- 基础设置 ---
            d-i debian-installer/locale string en_US.UTF-8
            d-i console-setup/ask_detect boolean false
            d-i keyboard-configuration/xkb-keymap select us
            d-i time/zone string Asia/Hong_Kong

            ### --- 网络配置 ---
            d-i netcfg/choose_interface select auto
            d-i netcfg/disable_dhcp boolean true
            d-i netcfg/get_ipaddress string {ip}
            d-i netcfg/get_netmask string {netmask}
            d-i netcfg/get_gateway string {gateway}
            d-i netcfg/get_nameservers string {dns}
            d-i netcfg/confirm_static boolean true

            ### --- 主机名与用户 ---
            d-i netcfg/get_hostname string {hostname}
            d-i netcfg/get_domain string local

            # Root 用户
            d-i passwd/root-password password {hashed_pw}
            d-i passwd/root-password-again password {hashed_pw}
            d-i passwd/root-login boolean true

            # 普通用户
            d-i passwd/make-user boolean true
            d-i passwd/user-fullname string User
            d-i passwd/username string debian
            d-i passwd/user-password-crypted password {hashed_pw}
            d-i user-uid string 1000

            ### --- 磁盘自动分区 ---
            d-i partman-auto/disk string /dev/sda
            d-i partman-auto/method string lvm
            d-i partman-auto-lvm/guided_size string max
            d-i partman-auto-lvm/new_vg_name string vg0
            d-i partman-auto/choose_recipe select atomic
            d-i partman/alignment string optimal
            d-i partman-lvm/device_remove_lvm boolean true
            d-i partman-md/device_remove_md boolean true
            d-i partman-partitioning/confirm_write_new_label boolean true
            d-i partman/confirm_write_new_label boolean true
            d-i partman-lvm/confirm boolean true
            d-i partman-lvm/confirm_nooverwrite boolean true
            d-i partman/choose_partition select finish
            d-i partman/confirm boolean true
            d-i partman/confirm_nooverwrite boolean true

            ### --- 软件与包管理 ---
            tasksel tasksel/first multiselect minimal
            d-i pkgsel/include string openssh-server
            d-i base-installer/install-recommends boolean false
            d-i pkgsel/install-language-support boolean false
            d-i pkgsel/upgrade select none
            popularity-contest popularity-contest/participate boolean false

            d-i mirror/country string manual
            d-i mirror/http/hostname string deb.debian.org
            d-i mirror/http/directory string /debian
            d-i mirror/http/proxy string

            ### --- GRUB 引导 ---
            d-i grub-installer/only_debian boolean true
            d-i grub-installer/bootdev string /dev/sda

            ### --- 完成安装 ---
            d-i finish-install/reboot_in_progress note
        """).strip()

        # 写入本地文件
        preseed_path = os.path.join(target_dir + '/12/', "preseed.cfg")
        with open(preseed_path, "w") as f:
            f.write(preseed)

        print(f"✅ [本地] 已生成 Debian preseed.cfg 到 {target_dir}/12/")

    else:
        raise RuntimeError(f"未知镜像类型: {iso_type}")