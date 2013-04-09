import re
import subprocess
import cloud

def ssh_info(jid):
    output = subprocess.check_output(
        "picloud ssh-info {0}".format(jid),
        shell=True,
        stderr=subprocess.STDOUT,
    )

    output = filter(None, output.split("\n"))

    try:
        return dict(zip( *[filter(None, re.split("\s+", l)) for l in output]))
    except:
        return None
    

# suppress ssh authenticity warnings?
# http://linuxcommando.blogspot.com/2008/10/how-to-disable-ssh-host-key-checking.html

def ssh_cmd(jid):
    return "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i {identity} {username}@{address} -p {port}".format(**cloud.shortcuts.ssh.get_ssh_info(jid))

def to_picloud_cmd(nb_name, jid):
    scp_to_command =  "scp -q -i {identity} -P {port} {nb_name} {username}@{address}:/home/picloud/notebook/".format(nb_name=nb_name, **cloud.shortcuts.ssh.get_ssh_info(jid))
    return scp_to_command



