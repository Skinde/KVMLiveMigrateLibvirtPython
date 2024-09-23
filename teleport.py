import sys
import libvirt
import time
domName = "ubuntu24.04"
conn = libvirt.open("qemu:///system")
if not conn:
    raise SystemExit("Failed to open connection to qemu:///system")

dom = None
try:
    dom = conn.lookupByName(domName)
except libvirtError as e:
    print(repr(e), file=sys.stderr)
    exit(1)

try:
   dest_conn = libvirt.open("qemu+ssh://client@192.168.18.73/system")
except libvirt.libvirtError as e:
    print(repr(e))
    exit(1)

prev_time = dom.getCPUStats(True)[0]['cpu_time']
time.sleep(1)
while True:
    current_time = dom.getCPUStats(True)[0]['cpu_time']
    usage = (current_time - prev_time)/10000000
    prev_time = current_time
    time.sleep(1)
    if usage>70:
        try:
            new_dom = dom.migrate(dest_conn, libvirt.VIR_MIGRATE_LIVE | libvirt.VIR_MIGRATE_PERSIST_DEST, None, None, 0)
            dest_conn.close()
            conn.close()
        except libvirt.libvirtError as e:
            print(repr(e), file=sys.stderr)
            exit(1)
        break
