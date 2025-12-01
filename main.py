import subprocess
import sys
from script.pre import generate_file ,encrypt_password



def run_packer_build():
    # 构建 packer 命令参数列表（推荐使用列表形式避免 shell 注入和空格问题）
    hostname = "tf-edu-ubuntu"
    vm_ip = "45.67.201.205"
    vm_gateway = "45.67.201.193"
    vm_netmask = "255.255.255.240"
    vm_dns = "8.8.8.8"
    ssh_username = "ubuntu"
    ssh_password = "test123"
    generate_file(
        hostname=hostname, ip=vm_ip, gateway=vm_gateway, netmask=vm_netmask, dns=vm_dns,
        user=ssh_username, password=ssh_password, iso_type="ubuntu"
    )
    cmd = [
        "packer", "build",
        "-var", "vsphere_server=10.4.10.140",
        "-var", "vsphere_user=root",
        "-var", "vsphere_password=Catixs@3202",
        "-var", "cluster=localhost",
        "-var", "datastore=HK_DATA",
        "-var", "network_name=VLAN 3917",
        "-var", "iso_path=[HK_DATA] ISO/ubuntu-22.04.5-live-server-amd64.iso",
        "-var", f"vm_name={hostname}",
        "-var", f"host_name={hostname}",
        "-var", "vm_cpus=2",
        "-var", "vm_ram=2048",
        "-var", "vm_disk_size=22144",
        "-var", f"ssh_host={vm_ip}",
        "-var", f"ssh_username={ssh_username}",
        "-var", f"ssh_password={encrypt_password(ssh_password)}",
        "./builds/ubuntu/22.04"
    ]

    try:
        # 执行命令并实时输出 stdout/stderr
        print("Running Packer build...")
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # 行缓冲
        )

        # 实时打印输出
        for line in process.stdout:
            print(line, end='')

        process.wait()

        if process.returncode == 0:
            print("\n✅ Packer build succeeded!")
        else:
            print(f"\n❌ Packer build failed with return code {process.returncode}")
            sys.exit(process.returncode)

    except FileNotFoundError:
        print("❌ Error: 'packer' command not found. Please ensure Packer is installed and in your PATH.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_packer_build()