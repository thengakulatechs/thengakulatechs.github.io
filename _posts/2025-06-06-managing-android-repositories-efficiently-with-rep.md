---
title: Managing Android Repositories Efficiently with Repo Tool
date: 2025-06-06 11:34:45 +0530
categories: [Version Control System, Repo, Android]
tags: [repo, git, android, devtools]
---

**Repo** is a tool built on top of Git that simplifies working with multiple repositories. It streamlines uploads to revision control systems, automates parts of the development workflow, and manages Git repositories efficiently.

> **Note:** Repo does **not** replace Git. Instead, it enhances Git usage in large, multi-repo projects like Android.
{: .prompt-tip }

The `repo` command is a Python script that you can place anywhere in your system’s `PATH`.

---

## 🛠️ Installation Guide

Repo installation consists of two parts:
1. A **launcher script**.
2. The **full Repo tool**, which is fetched during initialization.

### 🔁 Method 1: Install via APT (Debian/Ubuntu)

```bash
sudo apt-get update
sudo apt-get install repo
```
> This may not always provide the latest version.
{: .prompt-warning }

### 🔧 Method 2: Manual Installation

If `apt` doesn’t work or the version is outdated, install manually:
```bash
mkdir ~/bin
export PATH=~/bin:$PATH
```
📥 Download and Setup the Repo Launcher
```bash
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
```
🔐 (Optional) Verify the Signature
```bash
gpg --recv-key 8BB9AD793E8E6153AF0F9A4416530D5E920F5C65
curl https://storage.googleapis.com/git-repo-downloads/repo.asc | gpg --verify - ~/bin/repo
```
⚡ One-liner Installation
```bash
export REPO=$(mktemp /tmp/repo.XXXXXXXXX)
curl -o ${REPO} https://storage.googleapis.com/git-repo-downloads/repo
gpg --recv-key 8BB9AD793E8E6153AF0F9A4416530D5E920F5C65
curl -s https://storage.googleapis.com/git-repo-downloads/repo.asc | gpg --verify - ${REPO} && install -m 755 ${REPO} ~/bin/repo
```

## 🏁 Initializing a Repo Client

Create a working directory:
```bash
mkdir WORKING_DIRECTORY
cd WORKING_DIRECTORY
```

## 🧾 Configure Git Identity

```bash
git config --global user.name "Your Name"
git config --global user.email you@example.com
```
> Use a Google-linked email address for Gerrit code review.
{: .prompt-info }

## 🌐 Initialize Repo

```bash
repo init -u https://android.googlesource.com/platform/manifest
```
Or specify a branch:
```bash
repo init -u https://android.googlesource.com/platform/manifest -b master
```

## 📥 Downloading Android Source Code

Run:
```bash
repo sync
```

## ⚡ Speed Up Sync

```bash
repo sync -c -j8
```
> `-c` Sync current branch only\
> `-j8` Use 8 threads\
> `-q` Add this flag for quieter output
{: .prompt-tip }

## 🔽 Minimal Sync (Shallow Clone)

Use this to reduce bandwidth and sync time:
```bash
repo init --depth=1 -u https://android.googlesource.com/platform/manifest -b master
repo sync -f --force-sync --no-clone-bundle --no-tags -j$(nproc --all)
```

## 🧠 Partial Clones (Git 2.19+ Recommended)

```bash
repo init -u https://android.googlesource.com/platform/manifest -b master \
  --partial-clone --clone-filter=blob:limit=10M
```
> Ideal for low-latency networks — downloads objects only when needed.
{: .prompt-tip }

## 📡 Using a Local Mirror (Bandwidth Saver)

Create a local mirror to avoid repeated network downloads.

### 🪞 Step 1: Create the Mirror
```bash
mkdir -p /usr/local/aosp/mirror
cd /usr/local/aosp/mirror
repo init -u https://android.googlesource.com/mirror/manifest --mirror
repo sync
```
### 💻 Step 2: Create Clients from Mirror
```bash
mkdir -p /usr/local/aosp/master
cd /usr/local/aosp/master
repo init -u /usr/local/aosp/mirror/platform/manifest.git
repo sync
```
### 🔄 Step 3: Sync Mirror & Client
```bash
cd /usr/local/aosp/mirror
repo sync
cd /usr/local/aosp/master
repo sync
```
>Mirror can be shared via LAN (NFS, SSH, Git) or removable drives.
{: .prompt-tip }

## 🧹 Resetting the Repo Workspace

### 🔄 Discard Local Changes
```bash
repo forall -c "git reset --hard"
```
### 🧼 Full Clean (Untracked Files Too)
```bash
repo forall -c 'git reset --hard ; git clean -fdx'
```
### 🗑️ Hard Reset (Preserving .repo)
```bash
rm -rf * && repo sync -l
```

## 📚 References & Resources

📖<a href="https://source.android.com/setup/develop" target="_blank" rel="noopener noreferrer">Android Source Developer Guide – Google</a>\
💬<a href="https://stackoverflow.com/questions/5012163/how-to-discard-changes-using-repo" target="_blank" rel="noopener noreferrer">StackOverflow: Discard Changes Using Repo<a>