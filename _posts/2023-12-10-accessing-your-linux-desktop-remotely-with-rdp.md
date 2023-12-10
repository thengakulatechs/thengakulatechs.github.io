---
title: Accessing Your Linux Desktop Remotely with RDP
date: 2023-12-10 11:27:16 +0400
categories: [Remote Access, Linux]
tags: [rdp]
---
## Accessing Your Linux Desktop Remotely with RDP

Remotely working on your Linux machine can be convenient and efficient, especially with the familiar and widely supported RDP (Remote Desktop Protocol). This guide walks you through setting up and connecting to your Linux desktop remotely using XRDP, a free and powerful third-party server, regardless of your specific distribution.

### Setting Up XRDP

1. **Install XRDP:**

Open a terminal window and run the following command, replacing `YOUR_DISTRIBUTION` with your specific distribution's package manager command:

| Distribution | Package Manager Command |
|---|---|
| Ubuntu or Debian | `sudo apt install xrdp` |
| Fedora | `sudo dnf install xrdp` |
| Arch Linux | `sudo pacman -S xrdp` |
| openSUSE | `sudo zypper install xrdp` |

2. **Configure XRDP:**

Once installed, edit the XRDP configuration file using your preferred text editor:

```sh
sudo nano /etc/xrdp/xrdp.ini
```

Ensure the following lines are uncommented:

```
port=3389
enable_vsock=true
```

These lines set the port number to the standard RDP port (3389) and enable virtual sockets for better performance.

3. **Restart XRDP:**

After making changes, restart the XRDP service:

```sh
sudo systemctl restart xrdp
```

4. **Find Your IP Address:**

Run the following command to find your machine's IP address:

```sh
ifconfig
```

Look for the IP address assigned to your network interface (e.g., eth0 or enp0s3).

### Connecting to Your Desktop

1. **Install an RDP Client:**

Install an RDP client on the machine you'll be using to connect remotely. Popular options include:

* **Windows:** Microsoft Remote Desktop (built-in)
* **Linux:** Remmina (available in most repositories)
* **Mac:** Microsoft Remote Desktop or FreeRDP (third-party)
* **Android:** Microsoft Remote Desktop or RDP Client (third-party)
* **iOS:** Microsoft Remote Desktop or RDP Client (third-party)

2. **Launch the RDP Client:**

Open the RDP client and enter the following information:

* **Computer:** The IP address of your Linux machine.
* **User name:** The username you use to log in to your Linux machine.
* **Password:** The password for your Linux user account.

3. **Connect:**

Click "Connect" to establish a remote desktop connection. You may be prompted to accept a security certificate.

### Additional Notes

* **Firewall:** You may need to open port 3389 in your firewall to allow incoming RDP connections. Refer to your specific firewall configuration guide for instructions.
* **Troubleshooting:** If you encounter any issues connecting, consult the XRDP documentation or online troubleshooting resources.
* **Performance:** RDP can sometimes offer better performance and responsiveness compared to VNC, especially on slower connections.
* **Security:** Ensure you use strong passwords and configure XRDP securely to protect your remote access.

### Conclusion

Setting up RDP on your Linux machine allows you to access your desktop remotely from any device with an RDP client. This can be especially useful for working from home, collaborating with others, or accessing files from another location. Remember to adjust firewall settings and refer to online resources if you encounter any difficulties.
