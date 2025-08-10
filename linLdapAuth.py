#!/usr/bin/env python3

import sys
import re
import os
import fileinput
from shutil import copy2, which
from subprocess import check_call
from pathlib import Path

def main():
    if 'nobackup' not in sys.argv:
        Path("./backupAuthConf").mkdir(parents=False, exist_ok=True)
    if os.path.isfile('/etc/debian_version'):
        check_call(["apt", "install", "-y", "ldap-utils", "sssd", "sssd-tools", "sssd-ldap", "libpam-sss", "libnss-sss", "openssl"])
        check_call(["pam-auth-update", "--enable", "mkhomedir"])
        if os.path.isfile('/etc/astra_version'):
            if 'nobackup' not in sys.argv:
                copy2('/etc/pam.d/sshd', 'backupAuthConf')
            for line in fileinput.input(['/etc/pam.d/sshd'], inplace=True):
                print(re.sub(r"^session    required     pam_mkhomedir.so.*\s*$", "", line), end='')
            with open('/etc/pam.d/sshd', 'a', encoding='utf-8') as file:
                file.write('session    required     pam_mkhomedir.so skel=/etc/skel/\n')
    elif os.path.isfile('/etc/altlinux-release'):
        check_call(["apt-get", "install", "-y", "sssd-client", "openldap-clients", "sssd", "sssd-tools", "sssd-ldap", "openssl"])
        check_call(["control", "system-auth", "sss"])
        if 'nobackup' not in sys.argv:
            copy2('/etc/nsswitch.conf', f'{sys.argv[1]}')
            copy2('/etc/openssh/sshd_config', f'{sys.argv[1]}')
        for line in fileinput.input(['/etc/nsswitch.conf'], inplace=True):
            print(re.sub(r"^(passwd|shadow|group):.*\s*$", "", line), end='')
        with open('/etc/nsswitch.conf', 'a', encoding='utf-8') as file:
            file.write('passwd:     files systemd sss\nshadow:     tcb files sss\ngroup:      files systemd sss\n')
        for line in fileinput.input(['/etc/openssh/sshd_config'], inplace=True):
            print(re.sub(r"^UsePAM.*\s*$", "", line), end='')
    elif os.path.isfile('/etc/redhat-release'):
        check_call(["dnf", "install", "-y", "sssd-client", "openldap-clients", "sssd", "sssd-tools", "sssd-ldap", "oddjob", "oddjob-mkhomedir", "openssl"])
        if which('authselect'):
            check_call(["authselect", "select", "sssd", "with-mkhomedir", "--force"])
        elif which('authconfig'):
            check_call(["authconfig", "--enablesssdauth", "--enablesssd", "--enablemkhomedir", "--updateall"])
        check_call(["systemctl", "enable", "--now", "oddjobd"])
    elif os.path.isfile('/etc/SUSE-brand'):
        check_call(["zypper", "install", "-y", "sssd-client", "openldap2-client", "sssd", "sssd-tools", "sssd-ldap", "openssl"])
        if 'nobackup' not in sys.argv:
            copy2('/etc/nsswitch.conf', f'{sys.argv[1]}')
        for line in fileinput.input(['/etc/nsswitch.conf'], inplace=True):
            print(re.sub(r"^(passwd|shadow|group):.*\s*$", "", line), end='')
        with open('/etc/nsswitch.conf', 'a', encoding='utf-8') as file:
            file.write('passwd:     compat sss\nshadow:     compat sss\ngroup:      compat sss\n')
        check_call(["pam-config", "-a", "--sss"])
        check_call(["pam-config", "-a", "--mkhomedir"])
    if 'norestart' not in sys.argv:
        check_call(["systemctl", "restart", "sshd"])

if __name__ == '__main__':
    sys.exit(main())
