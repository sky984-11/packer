import subprocess
import sys
from script.pre import generate_file, encrypt_password


def run_packer_build():

    # 所有构建参数集中到一个字典，方便维护
    config = {
        "vm_name": "tf-debian",
        "vm_ip": "10.1.10.200",
        "vm_gateway": "10.1.10.1",
        "vm_netmask": "255.255.255.0",
        "vm_dns": "8.8.8.8",
        "ssh_username": "debian",
        "ssh_password": "test123",

        "vsphere_server": "10.1.10.18",
        "vsphere_user": "root",
        "vsphere_password": "Catixs@3202",
        "datastore": "datastore2_nvme",
        "network_name": "VLAN 10",
        "cluster": "localhost",

        "vm_cpus": "2",
        "vm_ram": "2048",
        "vm_disk_size": "20144",

        "os_type": "debian",
        "os_version": "12",

        "annotation": "Created by Packer"
    }

    # 生成 preseed/autoinstall 文件
    generate_file(
        hostname=config["vm_name"],
        ip=config["vm_ip"],
        gateway=config["vm_gateway"],
        netmask=config["vm_netmask"],
        dns=config["vm_dns"],
        user=config["ssh_username"],
        password=config["ssh_password"],
        iso_type=config["os_type"]
    )

    # 自动构建 packer -var 参数
    packer_vars = []
    for k, v in config.items():
        packer_vars.append("-var")
        packer_vars.append(f"{k}={v}")

    # ISO 路径（后续可扩展函数自动映射），需要和ESXI中镜像路径保持一致
    iso_path = f"[{config['datastore']}] ISO/{config['os_type']}-{config['os_version']}.iso"

    packer_vars.extend([
        "-var", f"iso_path={iso_path}",
        f"./builds/{config['os_type']}/{config['os_version']}"
    ])

    # 最终 Packager 命令
    cmd = ["packer", "build"] + packer_vars

    print("🚀 Running Packer build...\n")
    print("➡️ 执行命令：")
    print(" ".join(cmd), "\n")

    try:
        # 执行命令
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # 实时输出
        for line in process.stdout:
            print(line, end="")

        # 等待执行结束
        process.wait()

        if process.returncode == 0:
            print("\n🎉 Packer build succeeded!")
        else:
            print(f"\n❌ Packer build failed with return code {process.returncode}")
            sys.exit(process.returncode)

    except FileNotFoundError:
        print("❌ Error: 'packer' command not found. Please ensure it is installed and in PATH.")
        sys.exit(1)

    except Exception as e:
        print(f"🔥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_packer_build()
