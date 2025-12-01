import subprocess
import sys
from script.pre import generate_file 



def run_packer_build():
    # 构建 packer 命令参数列表（推荐使用列表形式避免 shell 注入和空格问题）
    generate_file(
    hostname="tf-edu-ubuntu", ip="10.4.10.100", gateway="10.4.10.1", netmask="255.255.255.0", dns="10.4.10.1",
    user="ubuntu", password="test123", iso_type="ubuntu"
    )
    cmd = [
        "packer", "build",
        "-var", "vsphere_server=10.4.10.140",
        "-var", "vsphere_user=root",
        "-var", "vsphere_password=Catixs@3202",
        "-var", "cluster=localhost",
        "-var", "datastore=HK_DATA",
        "-var", "network_name=VLAN 10",
        "-var", "iso_path=[HK_DATA] ISO/ubuntu-22.04.5-live-server-amd64.iso",
        "-var", "vm_name=tf-edu-ubuntu",
        "-var", "host_name=tf-edu-ubuntu",
        "-var", "vm_cpus=2",
        "-var", "vm_ram=2048",
        "-var", "vm_disk_size=22144",
        "-var", "ssh_username=ubuntu",
        "-var", f"ssh_password=$6$0ovtYUWS7QOv0tPi$E/vBi.DcAvKrheYl/3K0w/.ZlzD1MM6PGHa89c2jv7qA1pV//abEHMdpDfC1E27pFJ10t6cBt0Bt7Y9s7bwCO/",
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