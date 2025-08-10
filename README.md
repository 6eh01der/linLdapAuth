# linLdapAuth
Linux ldap authentication configuration

Required python version >=3.6. No dependencies - core library and nothing more.

This is just part of original script that contains specific functions that was developed for specific tasks and software. Presented "limited edition" able to install necessary packages (sssd, sssd-ldap and etc.) and configure nss, pam and ssh for ldap authentication.
Supported Linux distros: Ubuntu, Debian, Astra, SUSE and OpenSuse, Alt, RedHat and similar like CentOS, RedOS, AlmaLinux should work too.

```
python3 linLdapAuth.py
```
Original configuration files will be copied to the `backupAuthConfig` directory automatically created in the current working directory.
To NOT backup original configs use `nobackup` option:
```
python3 linLdapAuth.py nobackup
```
By default last step is sshd restart. To not restart it use `norestart`:
```
python3 linLdapAuth.py norestart
```

SSSD should be configured separately.
Example config:
```
[sssd]
domains=example.com
services=nss, pam, ssh

[domain/example.com]
cache_credentials=true
case_sensitive=false
enumerate=true
ldap_schema=ad
ldap_id_mapping=true
ldap_id_use_start_tls=true
ldap_tls_reqcert=never
id_provider=ldap
auth_provider=ldap
access_provider=simple
fallback_homedir = /home/%u@%d
use_fully_qualified_names=true
ldap_referrals=false
simple_allow_groups=GROUP
ldap_uri=ldaps://192.168.74.229:636
ldap_search_base=dc=example,dc=com?subtree?
ldap_default_bind_dn=CN=SEARCH_USER,CN=Users,DC=example,DC=com
ldap_default_authtok=PASSWORD
```

`PASSWORD`, `GROUP` and `SEARCH_USER` are just for example and must be changed.
