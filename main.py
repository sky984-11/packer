import subprocess
import sys
from script.pre import generate_file ,encrypt_password



def run_packer_build():
    # 构建 packer 命令参数列表（推荐使用列表形式避免 shell 注入和空格问题）
    host_name = "tf-edu-ubuntu"
    vm_ip = "45.67.201.205"
    vm_gateway = "45.67.201.193"
    vm_netmask = "255.255.255.240"
    vm_dns = "8.8.8.8"
    ssh_username = "ubuntu"
    ssh_password = "test123"

    vsphere_server = "10.4.10.140"
    vsphere_user = "root"
    vsphere_password = "Catixs@3202"
    datastore = "HK_DATA"
    network_name = "VLAN 3917"

    vm_cpus = "2"
    vm_ram = "2048"
    vm_disk_size = "22144"

    generate_file(
        hostname=host_name, ip=vm_ip, gateway=vm_gateway, netmask=vm_netmask, dns=vm_dns,
        user=ssh_username, password=ssh_password, iso_type="ubuntu"
    )
    cmd = [
        "packer", "build",
        "-var", f"vsphere_server={vsphere_server}",
        "-var", f"vsphere_user={vsphere_user}",
        "-var", f"vsphere_password={vsphere_password}",
        "-var", f"cluster=localhost",
        "-var", f"datastore={datastore}",
        "-var", f"network_name={network_name}",
        "-var", "iso_path=[DATA] ISO/ubuntu-22.04.5-live-server-amd64.iso",
        "-var", f"vm_name={host_name}",
        "-var", f"host_name={host_name}",
        "-var", f"vm_cpus={vm_cpus}",
        "-var", f"vm_ram={vm_ram}",
        "-var", f"vm_disk_size={vm_disk_size}",
        "-var", f"ssh_username={ssh_username}",
        "-var", f"ssh_password={ssh_password}",
        "-var", f"vm_ip={vm_ip}",
        "-var", f"vm_gateway={vm_gateway}",
        "-var", f"vm_netmask={vm_netmask}",
        "-var", f"vm_dns={vm_dns}",
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