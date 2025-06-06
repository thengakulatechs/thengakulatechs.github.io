---
title: How to Access Your Linux Desktop Remotely Using XRDP
date: 2025-06-06 12:56:38 +0530
categories: [Linux, Remote access]
tags: ['xrdp', 'remote-desktop', 'rdp', 'linux', 'ubuntu', 'systemd', 'firewall', 'security']
---

Remotely working on your Linux machine can be convenient and efficient, especially with the familiar and widely supported **RDP (Remote Desktop Protocol)**.  

This guide walks you through setting up and connecting to your Linux desktop remotely using **XRDP**, a free and powerful third-party RDP server, compatible with multiple Linux distributions.

---

## ⚙️ Setting Up XRDP on Linux

### 📦 Install XRDP
Open a terminal and run the appropriate command for your distribution:

| Distribution      | Command                          |
|-------------------|----------------------------------|
| **Ubuntu/Debian** | `sudo apt install xrdp`          |
| **Fedora**        | `sudo dnf install xrdp`          |
| **Arch Linux**    | `sudo pacman -S xrdp`            |
| **openSUSE**      | `sudo zypper install xrdp`       |

---

## 📝 Configure XRDP

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

## 🔄 Restart the XRDP Service

```bash
sudo systemctl restart xrdp
```
This applies any configuration changes.

## 🌐 Find Your IP Address

To connect to your Linux machine via RDP, you'll need to know its local IP address (on your LAN or network). There are multiple ways to find it, depending on your Linux setup.

### 🖥️ Option 1: Use ip or ifconfig (Terminal)
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
### 📋 Option 2: Use hostname -I
This is a quick and clean way to get just the IP address:
```bash
hostname -I
```
Output example:
```bash
192.168.1.42
```

### 🖱️ Option 3: Check via GUI (Graphical Interface)
If you’re running a desktop environment:
1. Open your Network Settings.
2. Click on the active connection (Wi-Fi or Ethernet).
3. Look for IPv4 Address or IP Address.

### 🧠 Know Your IP Context
- Local IP (e.g., 192.168.x.x, 10.x.x.x) is for devices on the same network.
- Public IP (e.g., 203.0.113.1) is for access outside your network.

> Use with caution — you’ll need proper security, port forwarding, or a VPN.
{: .prompt-warning }

To check your public IP, use:
```bash
curl ifconfig.me
```

### 🔁 Refreshing IP After Reboot
If you restart your Linux machine, its IP address may change (depending on DHCP settings). Consider setting a static IP address or using DHCP reservation on your router if you plan to access the machine frequently.

## 💻 Connecting to Your Linux Desktop

### 🔧 Install an RDP Client
Choose an RDP client based on your device:

- Windows: Microsoft Remote Desktop (built-in)
- Linux: Remmina
- macOS: Microsoft Remote Desktop (from App Store)
-Android/iOS: Microsoft Remote Desktop or other RDP clients

### 🚪 Launch and Configure the RDP Client
In your RDP client, enter:
- Computer: Your Linux machine’s IP address
- Username: Your Linux user name
- Password: Your Linux user password
Then click Connect.

> You may be prompted to accept a certificate — this is expected.
{: .prompt-warning }

## 🛠 Additional Notes

- 🔥 Firewall: Make sure port 3389 is open. For UFW (Ubuntu):
```bash
sudo ufw allow 3389/tcp
```

- ❓ Troubleshooting: If the session fails to start, try installing a desktop environment like XFCE:
```bash
sudo apt install xfce4
echo "startxfce4" > ~/.xsession
```
- ⚡ Performance: XRDP over RDP usually performs better than VNC, especially on slower networks.
- 🔐 Security Tip:
  - Use strong passwords.
  - Avoid exposing port 3389 directly to the internet.
  - Consider setting up an SSH tunnel or VPN for remote access.

## ✅ Conclusion

Using XRDP to set up RDP access on your Linux machine enables seamless remote work from almost any device. It’s ideal for:
- Working from home
- Remote troubleshooting
- File access across locations

Just make sure your system is secure, firewall rules are correct, and you use a reliable RDP client.