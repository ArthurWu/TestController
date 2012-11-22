from runner import get_config
from vm_host import HostServer
from vm import Vm
import json
from pysphere import VIServer

def revert_and_start():
    try:
        for host in get_hosts():
            server = VIServer()
            server.connect(host.ip, host.user, host.pwd)
            
            for vm_path in host.vms:
                try:
                    vm = server.get_vm_by_path(vm_path.strip())
                    vm.revert_to_snapshot()
                    if not vm.is_powered_on():
                        vm.power_on()
                except Exception, e:
                    print "[ERROR] Error happened when revert and start test lab %s" % vm_path
                    print e

            server.disconnect()
    except Exception, e:
        print "[ERROR] Error happened when prepare test enviroment(revert and start test labs)."
        print e
    else:
        print "[SECCESS] All test labs are reverted and started compleletely."

def get_hosts():
    labs = get_config().items('labs')
    return [Host( l[0], json.loads(l[1]) ) for l in labs]

class Host:
    def __init__(self, ip, info):
        self.ip = ip
        self.user = info['user']
        self.pwd = info['pwd']
        self.vms = info['vms']

# this method is used to get all the vms path for tester the set config.ini labs section
def get_vms_path(host):
    vi = VIServer()
    vi.connect(host, 'root', 'Pa$$word')
    all_vms_path = vi.get_registered_vms()
    print all_vms_path
    vi.disconnect()

if __name__ == '__main__':
    print 'revert...'
    #revert_and_start()
