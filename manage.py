import libvirt
import sys


conn = libvirt.open("qemu:///system")

def start_vm():
    vm = conn.lookupByName("ubuntu24.04")
    if not vm.isActive():
        vm.create()

def stop_vm():
    vm = conn.lookupByName("ubuntu24.04")
    if vm.isActive():
        vm.shutdown()

if (sys.argv[1] == "start"):
    start_vm()
if (sys.argv[1] == "stop"):
    stop_vm()
