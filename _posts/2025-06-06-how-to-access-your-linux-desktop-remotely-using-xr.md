---
title: How to Access Your Linux Desktop Remotely Using XRDP
date: 2025-06-06 12:56:38 +0530
categories: [Linux, Remote access]
tags: ['xrdp', 'remote-desktop', 'rdp', 'linux', 'ubuntu', 'systemd', 'firewall', 'security']
---

Remotely working on your Linux machine can be convenient and efficient, especially with the familiar and widely supported **RDP (Remote Desktop Protocol)**.  

This guide walks you through setting up and connecting to your Linux desktop remotely using **XRDP**, a free and powerful third-party RDP server, compatible with multiple Linux distributions.

---

## Setting Up XRDP on Linux

### Install XRDP
Open a terminal and run the appropriate command for your distribution:

| Distribution      | Command                          |
|-------------------|----------------------------------|
| **Ubuntu/Debian** | `sudo apt install xrdp`          |
| **Fedora**        | `sudo dnf install xrdp`          |
| **Arch Linux**    | `sudo pacman -S xrdp`            |
| **openSUSE**      | `sudo zypper install xrdp`       |

---

## Configure XRDP

After installing XRDP, open the configuration file:

```bash
sudo nano /etc/xrdp/xrdp.ini
```
Ensure the following lines are uncommented and configured:
```sh
port=3389
enable_vsock=true
```

> `port=3389` sets the standard RDP port.\
> `enable_vsock=true` enables efficient communication for local virtual machines.
{: .prompt-info }

## Restart the XRDP Service

```bash
sudo systemctl restart xrdp
```
This applies any configuration changes.

## Find Your IP Address

To connect to your Linux machine via RDP, you'll need to know its local IP address (on your LAN or network). There are multiple ways to find it, depending on your Linux setup.

### Option 1: Use ip or ifconfig (Terminal)
Recommended command (modern and widely supported):
```shell
ip addr show
```

> Here’s an example output from running ip addr show on a Linux system:
```shell
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
>       
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 52:54:00:12:34:56 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0
       valid_lft 86398sec preferred_lft 86398sec
    inet6 fe80::5054:ff:fe12:3456/64 scope link 
       valid_lft forever preferred_lft forever
```
{: .prompt-info }

> Explanation:\
**lo** – the loopback interface (`127.0.0.1`)\
**eth0** – an Ethernet interface with IP address `192.168.1.100`\
**inet** – IPv4 address\
**inet6** – IPv6 address\
**state UP** – the interface is active\
**mtu** – Maximum Transmission Unit\
**link/ether** – MAC address
{: .prompt-tip }

Look for an entry under your active network interface (eth0, enp0s3, or wlan0) that looks like this:
```shell
inet 192.168.1.42/24
```
The IP address is: `192.168.1.42`
> This method works across most Linux distributions.
{: .prompt-tip }

Legacy command (still works on many systems):
```bash
ifconfig
```
If ifconfig is not found, you may need to install it:
```bash
sudo apt install net-tools   # For Ubuntu/Debian
```
### Option 2: Use hostname -I
This is a quick and clean way to get just the IP address:
```bash
hostname -I
```
Output example:
```bash
192.168.1.42
```

### Option 3: Check via GUI (Graphical Interface)
If you’re running a desktop environment:
1. Open your Network Settings.
2. Click on the active connection (Wi-Fi or Ethernet).
3. Look for IPv4 Address or IP Address.

### Bonus: Find Your Public IP
If you want to connect from a different network (e.g., over the internet), you’ll need your public IP:
```bash
curl ifconfig.me
```

### Know Your IP Context
- Local IP (e.g., 192.168.x.x, 10.x.x.x) is for devices on the same network.
- Public IP (e.g., 203.0.113.1) is for access outside your network.

> Use with caution — you’ll need proper security, port forwarding, or a VPN.
{: .prompt-warning }

To check your public IP, use:
```bash
curl ifconfig.me
```

### Refreshing IP After Reboot
If you restart your Linux machine, its IP address may change (depending on DHCP settings). Consider setting a static IP address or using DHCP reservation on your router if you plan to access the machine frequently.

## Firewall Configuration

Make sure your firewall allows RDP traffic on port 3389:
```bash
sudo ufw allow 3389/tcp
```
To check firewall status:
```bash
sudo ufw status
```

## Connecting to Your Linux Desktop

### Install an RDP Client
Choose an RDP client based on your device:

| Platform      | Recommended RDP Client                     |
|---------------|--------------------------------------------|
| **Windows**   | `Microsoft Remote Desktop (built-in)`      |
| **Linux**     | `Remmina`                                  |
| **macOS**     | `Microsoft Remote Desktop (Mac App Store)` |
| **Android**   | `Microsoft Remote Desktop / RD Client`     |
| **iOS**       | `Microsoft Remote Desktop / RD Client`     |

### Launch and Configure the RDP Client

In your RDP client, enter:
- Computer: Your Linux machine’s IP address
- Username: Your Linux user name
- Password: Your Linux user password
Then click Connect.

> You may be prompted to accept a certificate — this is expected.
{: .prompt-warning }

## Optional: Install a Lightweight Desktop (If Needed)
Some server distributions don’t include a graphical environment. You can install a lightweight desktop such as XFCE:
```bash
sudo apt install xfce4
echo "startxfce4" > ~/.xsession
```
Restart XRDP:
```bash
sudo systemctl restart xrdp
```

## Additional Notes

- Firewall: Make sure port 3389 is open. For UFW (Ubuntu):
```bash
sudo ufw allow 3389/tcp
```

- Troubleshooting: If the session fails to start, try installing a desktop environment like XFCE:
```bash
sudo apt install xfce4
echo "startxfce4" > ~/.xsession
```
- Performance: XRDP over RDP usually performs better than VNC, especially on slower networks.
- Security Tip:
  - Use strong passwords.
  - Avoid exposing port 3389 directly to the internet.
  - Consider setting up an SSH tunnel or VPN for remote access.
- Black Screen After Login?
Make sure your user has a proper .xsession file and that the desktop environment is installed.
- Cannot Reconnect After Disconnect?
Try restarting the XRDP and session manager services:
```bash
sudo systemctl restart xrdp
sudo systemctl restart xrdp-sesman
```
- Security Warning or Certificate Error?
Accept the certificate if it's your system. For public access, consider using a custom certificate and SSH tunneling.

## Security Best Practices
If you're enabling RDP access over the internet:
- Use strong passwords
- Consider using SSH tunneling or VPN instead of exposing port 3389
- Restrict RDP to known IP ranges via firewall rules
- Enable logging and auditing on XRDP and SSH

## Conclusion

XRDP makes it easy to connect to your Linux desktop from almost any device using the familiar RDP protocol. Whether you're managing a remote server, helping a colleague, or accessing your home machine on the go, this setup provides flexibility and performance with minimal configuration. With proper firewall, security, and desktop environment setup, you can enjoy a smooth remote experience. Just make sure your system is secure, firewall rules are correct, and you use a reliable RDP client.

## References

<a href="https://www.xrdp.org/" target="_blank" rel="noopener noreferrer">XRDP Official Site</a>\
<a href="https://remmina.org/" target="_blank" rel="noopener noreferrer">Remmina – Remote Desktop for Linux</a>\
<a href="https://help.ubuntu.com/community/UFW/" target="_blank" rel="noopener noreferrer">Ubuntu Firewall Configuration</a>\
<a href="https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remotepc/remote-desktop-allow-access/" target="_blank" rel="noopener noreferrer">Enable Remote Desktop on your PC</a>