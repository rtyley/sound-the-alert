## Root setup

```
$ mount | grep mmc
/dev/mmcblk0p2 on /media/roberto/ec2aa3d2-eee7-454e-8260-d145df5ddcba type ext4 (rw,nosuid,nodev,relatime,data=ordered,uhelper=udisks2)

$ sudo -i
$ cd /media/roberto/ec2aa3d2-eee7-454e-8260-d145df5ddcba

# devname=octoalert-3

# printf "$devname\n" > etc/hostname ; cat etc/hostname
octoalert-3

# sed -i s/raspberrypi/$devname/g etc/hosts ; cat etc/hosts
127.0.0.1	localhost
::1		localhost ip6-localhost ip6-loopback
ff02::1		ip6-allnodes
ff02::2		ip6-allrouters

127.0.1.1	octoalert-3

$ grep "iface eth0" -A2 etc/network/interfaces
iface eth0 inet static
        address 169.254.0.103/24


# cat ~roberto/development/sound-the-alert/wpa_supplicant.networks.conf >> etc/wpa_supplicant/wpa_supplicant.conf ; cat etc/wpa_supplicant/wpa_supplicant.conf
```

#### Disable SSH Password_Authentication

https://help.ubuntu.com/community/SSH/OpenSSH/Configuring#Disable_Password_Authentication

```
# printf "PasswordAuthentication no\n" >> etc/ssh/sshd_config ; grep "^PasswordAuthentication" etc/ssh/sshd_config
PasswordAuthentication no
```

## Non-root setup

Enable SSH by creating a `/boot/ssh` file (see http://raspberrypi.stackexchange.com/a/62456/6462 and https://www.raspberrypi.org/blog/a-security-update-for-raspbian-pixel/ ):

```
$ touch /media/roberto/boot1
```

```
$ cd home/pi/
$ mkdir .ssh ; cp ~/.ssh/authorized_keys .ssh/authorized_keys
$ git clone git@github.com:rtyley/sound-the-alert.git
```


```
sudo raspi-config
sudo reboot
```

