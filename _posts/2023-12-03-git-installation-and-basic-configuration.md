---
title: Git Installation and Basic Configuration
date: 2023-12-03 14:57:36 +0400
categories: [Version Control System, Git]
tags: [git]
---
## Installation
Installing Git: A Simplified Guide for Linux, macOS, and Windows

[Linux](https://git-scm.com/download/linux)
Using Terminal

```sh
sudo apt install git \\Debian
sudo dnf install git \\Fedora 22 and later
sudo yum install git \\Red Hat
sudo pacman -S git \\Arch
```
[MacOS](https://git-scm.com/download/mac)
Using Terminal

```sh
xcode-select --install \\Using Xcode
brew install git \\using Homebrew
```
[Windows](https://git-scm.com/download/win)

Download and install Windows setup from [here](https://git-scm.com/download/win)

[Winget](https://github.com/microsoft/winget-cli)
Use CMD or Terminal
```sh
winget install git
```

Using Command line or PowerShell ([Chocolatey](https://chocolatey.org/install))

```sh
choco install git.install \\Using Chocolatey
```

## Basic Configuration

Setup user name and email address:
```sh
git config --global user.name "Your Name"
git config --global user.email yourname@example.com
```

Setup editor:

Linux/MacOS
```sh
git config --global core.editor nano
```
Windows
```sh
git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"
```

View configurations:
```sh
git config --list
```

## Git Usage

```sh
git init
```

**git init** - Create an empty Git repository or reinitialize an existing one