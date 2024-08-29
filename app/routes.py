from flask import render_template, request, redirect, url_for
from app import app
from app.ssh_utils import ssh_connect, ssh_config
import paramiko  
from paramiko import SSHException
from app.ssh_utils import ssh_connect 
from app.ssh_utils import ssh_config 


@app.route('/dashboard')
def dashboard():
    vm_status = {} 

    for vm_name, ssh_info in ssh_config.items():
        try:
            ssh_client = ssh_connect(ssh_info['hostname'], ssh_info['username'], ssh_info['password'])
            if ssh_client:
                vm_status[vm_name] = 'Connecté'
        except paramiko.ssh_exception.SSHException:
            vm_status[vm_name] = 'Échec de la connexion'
        except Exception as e:
            vm_status[vm_name] = 'Erreur: ' + str(e)

    return render_template('dashboard.html', vm_status=vm_status)

def get_vm_info(vm_id):
    if vm_id in ssh_config:
        ssh_info = ssh_config[vm_id]
        vm_info = {'name': vm_id, 'ip': ssh_info['hostname'], 'ping': 'N/A'}
        ssh_client = ssh_connect(ssh_info['hostname'], ssh_info['username'], ssh_info['password'])
        if ssh_client:
            try:
                stdin, stdout, stderr = ssh_client.exec_command('ping -c 1 google.com')
                ping_output = stdout.read().decode('utf-8')
                ping_time = ping_output.split('time=')[1].split(' ')[0]
                vm_info['ping'] = ping_time + ' ms'
            except Exception as e:
                pass
            finally:
                ssh_client.close()

        return vm_info

    return None 


@app.route('/editvm/<vm_id>')
def edit_vm(vm_id):
    vm_info = get_vm_info(vm_id)
    if vm_info:
        return render_template('editvm.html', vm_info=vm_info)
    else:
        return "Machine non trouvée"
    
import os

def get_vm_config(vm_id):
    config_file = os.path.expanduser('sshconfig.json')

    config = paramiko.SSHConfig()
    config.parse(open(config_file))

    host_info = config.lookup(vm_id)

    if 'hostname' in host_info:
        vm_ip = host_info['hostname']
    else:
        raise Exception("Host not found in SSH Config")

    if 'user' in host_info:
        username = host_info['user']
    else:
        raise Exception("Username not found in SSH Config")

    if 'port' in host_info:
        port = int(host_info['port'])
    else:
        port = 22  # Utilisez le port par défaut si non spécifié dans SSH Config

    return {
        'vm_ip': vm_ip,
        'username': username,
        'port': port  # Vous pouvez renvoyer le port si nécessaire
    }
