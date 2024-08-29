import paramiko
import json
with open('sshconfig.json', 'r') as config_file:
    ssh_config = json.load(config_file)

def ssh_connect(hostname, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname, username=username, password=password)
        return ssh_client
    except paramiko.AuthenticationException:
        return None

def is_vm_online(vm_name):
    if vm_name in ssh_config:
        ssh_info = ssh_config[vm_name]
        ssh_client = ssh_connect(ssh_info['hostname'], ssh_info['username'], ssh_info['password'])
        if ssh_client:
            ssh_client.close()
            return True
    return False


