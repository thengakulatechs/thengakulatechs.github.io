---
title: Complete Guide - Installing Arch Linux on Encrypted LUKS Volume with UEFI and systemd
date: 2025-09-27 01:17:29 +0530
categories: [Linux, System Administration]
tags: ['arch-linux', 'luks', 'encryption', 'uefi', 'systemd', 'security']
---

Full disk encryption has become essential for securing sensitive data on modern systems. This comprehensive guide demonstrates the installation of Arch Linux on a LUKS-encrypted volume, leveraging UEFI boot capabilities and systemd-boot for modern system management. This configuration provides robust data protection while maintaining optimal system performance.

**Note**: If you want a simpler encryption setup or prefer LVM on LUKS, you can use the [archinstall](https://wiki.archlinux.org/title/Archinstall) "guided" installer included with Arch since April 2021, or refer to alternative configurations using LVM for more complex storage management.

## USB Preparation and Boot

Download the latest Arch Linux ISO from the official [website](https://archlinux.org/download/). Prepare your installation medium following proper verification procedures.
If you downloaded Arch Linux from a mirror, ensure you verify the file's checksum:

```shell
sha1sum archlinux-version-x86_64.iso
md5sum archlinux-version-x86_64.iso
```
Compare these checksums with the official Arch Linux checksums for verification. [Verify signature](https://wiki.archlinux.org/title/Installation_guide#Verify_signature)

Find your USB drive with `lsblk` and ensure it's not mounted. Write the ISO to your USB drive (replace `/dev/sdx` with your actual drive):

```shell
dd bs=4M if=path/to/archlinux-version-x86_64.iso of=/dev/sdx conv=fsync oflag=direct status=progress
```
On Windows use [Rufus](https://rufus.ie/en/#download)

## System Preparation

Boot from the USB drive. Ensure Secure Boot is disabled in your BIOS/UEFI settings if boot fails.

## Set the console keyboard layout and font

The default console keymap is US. Available layouts can be listed with:

```shell
localectl list-keymaps
```

### localectl list-keymaps
To set the keyboard layout, pass its name to loadkeys. For example, to set a German keyboard layout:

```shell
loadkeys de-latin1
```

If the current font is unreadable or too small, change it:

```shell
setfont sun12x22
```

Verify UEFI mode is active:

```shell
ls /sys/firmware/efi/efivars
```

If no errors occur and the directory exists, you're running in UEFI mode. Otherwise, reboot and enable UEFI mode in your firmware settings.
Establish internet connectivity. For wired connections, this should be automatic. For wireless:

```shell
iwctl
[iwd]# device list
[iwd]# station wlan0 scan
[iwd]# station wlan0 get-networks
[iwd]# station wlan0 connect "Your_SSID"
[iwd]# exit
```
Alternatively, you can supply it as a command line argument:

```shell
iwctl --passphrase *passphrase* station *name* connect *SSID*
```
Example:
```shell
iwctl --passphrase mypassw0rd station wlan1 connect Home-01
```

Test connectivity and update system clock:

```shell
ping -c 3 archlinux.org
timedatectl set-ntp true
timedatectl status
```

Optionally, modify `/etc/pacman.d/mirrorlist` to prioritize geographically closer mirrors. This file will be copied to your final system.

## Disk Partitioning

Identify your target disk:

```shell
lsblk
```

The target should be something like `/dev/sda` or `/dev/nvme0n1`.

**Security Note**: Optionally shred the disk to remove any previous data:

```shell
shred -v -n1 /dev/sda
```

Partition the disk using `gdisk` for GPT partitioning:

```shell
gdisk /dev/sda
```

Create the following partition scheme:
- **Partition 1**: EFI System Partition (512MB, type ef00)
- **Partition 2**: Linux LVM partition (remaining space, type 8e00)

Detailed gdisk commands:
```shell
o          # Create new GPT partition table
n          # New partition
1          # Partition number
[Enter]    # Default start sector
+512M      # 512MB for EFI
ef00       # EFI System partition type

n          # New partition
2          # Partition number
[Enter]    # Default start sector
[Enter]    # Use remaining space
8e00       # Linux LVM partition type

w          # Write changes
y          # Confirm changes
```

Format the EFI partition:

```shell
mkfs.fat -F32 /dev/sda1
```

## LUKS Encryption and LVM Setup

Load the dm-crypt kernel module:

```shell
modprobe dm-crypt
```

Initialize LUKS2 encryption on the LVM partition:

```shell
cryptsetup luksFormat --type luks2 /dev/sda2
```

You'll be prompted to confirm and set a strong passphrase. Choose a secure passphrase you can remember - this will be required on every boot.

Open the encrypted container:

```shell
cryptsetup open /dev/sda2 cryptlvm
```

Verify the mapping was created:

```shell
ls -la /dev/mapper/cryptlvm
```

Now configure LVM on the encrypted volume:

```shell
# Create physical volume
pvcreate /dev/mapper/cryptlvm

# Create volume group
vgcreate volume /dev/mapper/cryptlvm

# Create logical volumes
lvcreate -L20G volume -n swap
lvcreate -L40G volume -n root
lvcreate -l 100%FREE volume -n home
```

Verify the LVM setup:

```shell
vgdisplay
lvdisplay
```

## Filesystem Creation and Mounting

Create filesystems on the logical volumes:

```shell
# Format logical volumes
mkfs.ext4 /dev/volume/root
mkfs.ext4 /dev/volume/home
mkswap /dev/volume/swap
```

Mount the filesystems in proper hierarchy:

```shell
# Mount root filesystem
mount /dev/volume/root /mnt

# Create and mount directories
mkdir /mnt/home
mkdir /mnt/boot
mount /dev/volume/home /mnt/home
mount /dev/sda1 /mnt/boot

# Enable swap
swapon /dev/volume/swap
```

## Base System Installation

Install essential packages. The selection includes base system, development tools, LVM support, and critical components for encrypted systems:

```shell
pacstrap /mnt base base-devel linux linux-firmware linux-headers lvm2 vim networkmanager
```

Generate the filesystem table:

```shell
genfstab -U /mnt >> /mnt/etc/fstab
```

Verify the fstab entries look correct:

```shell
cat /mnt/etc/fstab
```

## System Configuration in chroot

Enter the new system environment:

```shell
arch-chroot /mnt
```

Configure timezone (adjust for your location):

```shell
ln -sf /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime
hwclock --systohc
```

Configure localization. Edit `/etc/locale.gen` and uncomment your preferred locale (e.g., `en_US.UTF-8 UTF-8`):

```shell
vim /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
```

Set keyboard layout (if not US):

```shell
echo "KEYMAP=us" > /etc/vconsole.conf
```

Configure hostname and networking:

```shell
echo "your-hostname" > /etc/hostname

cat << EOF > /etc/hosts
127.0.0.1   localhost
::1         localhost
127.0.1.1   your-hostname.localdomain your-hostname
EOF
```

## Critical Encryption Configuration

Configure the initial ramdisk to support encryption. This is crucial for the system to boot properly.

Edit `/etc/mkinitcpio.conf`:

```shell
vim /etc/mkinitcpio.conf
```

Modify the `HOOKS` line to include encryption and LVM support. The order is critical:

```text
HOOKS=(base udev autodetect keyboard keymap consolefont modconf block encrypt lvm2 filesystems fsck)
```

Add keyboard support to modules for external keyboards during boot:

```text
MODULES=(ext4)
```

Regenerate the initramfs:

```shell
mkinitcpio -p linux
```

## User Management and Root Password

Set the root password:

```shell
passwd
```

Create a regular user account:

```shell
useradd -m -G wheel -s /bin/bash username
passwd username
```

Configure sudo access by editing the sudoers file:

```shell
EDITOR=vim visudo
```

Uncomment the line: `%wheel ALL=(ALL:ALL) ALL`

## systemd-boot Configuration

Install systemd-boot to the EFI system partition:

```shell
bootctl install
```

Configure the boot loader:

```shell
cat << EOF > /boot/loader/loader.conf
default arch.conf
timeout 3
console-mode max
editor no
EOF
```

The `editor no` prevents boot parameter modification at startup for security.

Create the boot entry. First, get the UUID of your encrypted partition:

```shell
blkid /dev/sda2
```

Create the boot entry file:

```shell
cat << EOF > /boot/loader/entries/arch.conf
title   Arch Linux
linux   /vmlinuz-linux
initrd  /initramfs-linux.img
options cryptdevice=UUID=your-actual-uuid:cryptlvm root=/dev/volume/root rw quiet
EOF
```

**Important**: Replace `your-actual-uuid` with the actual UUID from the `blkid` command output.

## Essential Services and Network Configuration

Install and enable critical services:

```shell
# Install essential packages if not already present
pacman -S sudo networkmanager openssh

# Enable services
systemctl enable NetworkManager
systemctl enable sshd
systemctl enable systemd-boot-update.service
```

## CPU Microcode Installation

Install appropriate microcode for your processor:

**For Intel CPUs:**
```shell
pacman -S intel-ucode
```

**For AMD CPUs:**
```shell
pacman -S amd-ucode
```

After installation, regenerate the boot configuration:

```shell
bootctl update
```

## Final Steps and Reboot

Exit the chroot environment:

```shell
exit
```

Unmount all filesystems:

```shell
umount -R /mnt
```

Close the encrypted volume and LVM:

```shell
vgchange -an
cryptsetup close cryptlvm
```

Reboot the system:

```shell
reboot
```

## Post-Installation Boot Process

During boot, you'll experience the following sequence:

1. **systemd-boot menu**: Select "Arch Linux" (or wait for timeout)
2. **LUKS passphrase prompt**: Enter your encryption passphrase
3. **System boot**: Normal Arch Linux boot process
4. **Login prompt**: Log in with your user account

## Advanced Security Enhancements

### Multiple LUKS Key Slots

LUKS supports multiple authentication methods. Add additional passphrases or key files:

```shell
# Add a second passphrase
sudo cryptsetup luksAddKey /dev/sda2

# Generate and add a key file (store securely)
sudo dd if=/dev/urandom of=/etc/luks-backup-key bs=512 count=4
sudo chmod 000 /etc/luks-backup-key
sudo cryptsetup luksAddKey /dev/sda2 /etc/luks-backup-key
```

### Performance Optimization

For SSD drives, enable periodic TRIM:

```shell
sudo systemctl enable fstrim.timer
```

Monitor encryption performance:

```shell
sudo cryptsetup benchmark
```

### Backup LUKS Headers

Create a backup of your LUKS header (store offline securely):

```shell
sudo cryptsetup luksHeaderBackup /dev/sda2 --header-backup-file luks-header-backup.bin
```

## Troubleshooting Common Issues

### Boot Problems

**No encryption prompt appears:**
- Verify `encrypt` hook is in mkinitcpio.conf
- Ensure hooks are in correct order
- Regenerate initramfs: `sudo mkinitcpio -p linux`

**Wrong UUID error:**
- Verify UUID in boot entry matches `blkid` output
- Ensure no typos in the boot configuration

**Keyboard not working at encryption prompt:**
- Add `keyboard` and `keymap` to mkinitcpio HOOKS
- Include `usbhid` and `xhci_hcd` in MODULES for USB keyboards

### Performance Issues

**Slow boot times:**
- Consider using key files for automatic unlocking (security trade-off)
- Optimize SSD performance with proper mount options

**System responsiveness:**
- Ensure SSD TRIM is enabled
- Monitor disk I/O with `iotop`

## Maintenance and Updates

Regular maintenance ensures continued security and performance:

```shell
# Update the system
sudo pacman -Syu

# Update boot loader
sudo bootctl update

# Check LUKS header integrity
sudo cryptsetup luksDump /dev/sda2
```

## Security Considerations

This installation provides strong data protection through full disk encryption. Consider these additional security measures for enhanced protection:

- **Regular backups**: Maintain encrypted backups of important data
- **Key management**: Store LUKS header backups and recovery keys securely offline  
- **System hardening**: Implement additional security measures like AppArmor or SELinux
- **Secure Boot**: Configure Secure Boot with custom keys for additional protection

The combination of LUKS2 encryption, UEFI secure boot capabilities, and systemd-boot provides a modern, secure foundation for your Arch Linux system. The simplified partition layout reduces complexity while maintaining strong security, making this configuration ideal for laptops and workstations requiring data protection.

Stay current with security updates and consider your specific threat model when implementing additional hardening measures.