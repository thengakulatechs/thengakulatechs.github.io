---
title: Repo Installation and Basic Configuration
date: 2023-12-03 15:12:29 +0400
categories: [Version Control System, Repo]
tags: [git]
---
Repo is a tool built on top of Git. Repo helps manage many Git repositories, does the uploads to revision control systems, and automates parts of the development workflow. Repo is not meant to replace Git, only to make it easier to work with Git. The repo command is an executable Python script that you can put anywhere in your path.

### Installation
Repo comes in two parts: One is a launcher script you install, and it communicates with the second part, the full Repo tool included in a source code checkout.
To install Repo,<br />follow these steps.

```sh
 sudo apt-get update
 sudo apt-get install repo
```

If those commands didn’t work for your system–for example, you see that the package version is outdated, or there isn’t an official package available from your Linux distribution, manually install Repo using the following commands:

```sh
mkdir ~/bin
PATH=~/bin:$PATH
```
Download the Repo Launcher and ensure that it’s executable:

```sh
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
```

Optionally verify the launcher matches our signatures:

```sh
gpg --recv-key 8BB9AD793E8E6153AF0F9A4416530D5E920F5C65
curl https://storage.googleapis.com/git-repo-downloads/repo.asc | gpg --verify - ~/bin/repo
```
Or Simply use:

```sh
export REPO=$(mktemp /tmp/repo.XXXXXXXXX)
curl -o ${REPO} https://storage.googleapis.com/git-repo-downloads/repo
gpg --recv-key 8BB9AD793E8E6153AF0F9A4416530D5E920F5C65
curl -s https://storage.googleapis.com/git-repo-downloads/repo.asc | gpg --verify - ${REPO} && install -m 755 ${REPO} ~/bin/repo
```

### Initializing a Repo client

After installing the Repo Launcher, set up your client to access the Android source repository, create an empty directory to hold your working files. Give it any name you like:

```sh
mkdir WORKING_DIRECTORY
cd WORKING_DIRECTORY
```
Configure Git with your real name and email address. To use the Gerrit code-review tool, you need an email address that's connected with a registered Google account. Ensure that this is a live address where you can receive messages. The name that you provide here shows up in attributions for your code submissions.

```sh
git config --global user.name Your Name
git config --global user.email you@example.com
```
Run `repo init` to get the latest version of Repo with its most recent bug fixes. You must specify a URL for the manifest, which specifies where the various repositories included in the Android source are placed within your working directory.

```sh
repo init -u https://android.googlesource.com/platform/manifest
```
To check out the master branch:

```sh
repo init -u https://android.googlesource.com/platform/manifest -b master
```

### Downloading the Android source tree

To download the Android source tree to your working directory from the repositories as specified in the default manifest, run:

```sh
repo sync
```
To speed syncs, pass the -c (current branch) and -jthreadcount flags:

```sh
repo sync -c -j8
```

The Android source files are downloaded in your working directory under their project names.
To suppress output, pass the -q (quiet) flag

### Minimal Sync

```sh
repo init --depth=1 -u https://android.googlesource.com/platform/manifest -b master
repo sync  -f --force-sync --no-clone-bundle --no-tags -j$(nproc --all)
```

If using Git version 2.19 or greater, you can specify –partial-clone when performing repo init which will make use of Git’s partial clone capability, which only downloads Git objects when needed instead of downloading everything. Because using partial clones means that many operations need to communicate with the server, this is recommended for developers who are using a network with low latency:

```sh
repo init -u https://android.googlesource.com/platform/manifest -b master --partial-clone --clone-filter=blob:limit=10M
``` 

### Using a local mirror 

When using several clients, especially in situations where bandwidth is scarce, it's better to create a local mirror of the entire server content, and to sync clients from that mirror (which requires no network access). The download for a full mirror is smaller than the download of two clients, and it contains more information.

These instructions assume that the mirror is created in /usr/local/aosp/mirror. First, create and sync the mirror itself. Notice the --mirror flag, which you can specify only when creating a new client:

```sh
mkdir -p /usr/local/aosp/mirror
cd /usr/local/aosp/mirror
repo init -u https://android.googlesource.com/mirror/manifest --mirror
repo sync
```
When the mirror is synced, you can create new clients from it. Note that you must specify an absolute path:

```sh
mkdir -p /usr/local/aosp/master
cd /usr/local/aosp/master
repo init -u /usr/local/aosp/mirror/platform/manifest.git
repo sync
```
Finally, to sync a client against the server, sync the mirror against the server, then the client against the mirror:

```sh
cd /usr/local/aosp/mirror
repo sync
cd /usr/local/aosp/master
repo sync
```
It's possible to store the mirror on a LAN server and to access it over NFS, SSH, or Git. It's also possible to store it on a removable drive and to pass that drive among users or machines.

### Repo Reset

Discard changes using repo tool.

```sh
repo forall -c "git reset --hard"
```
If there is a need to revert working folder to the clean state where you don’t have local modifications and no untracked files.

```sh
repo forall -c 'git reset --hard ; git clean -fdx'
```
Alternative methods:

```sh
rm -rf * ; repo sync -l
```
Note that .repo is preserved after that.

### Reference
[Google](https://source.android.com/setup/develop)
[Stackoverflow](https://stackoverflow.com/questions/5012163/how-to-discard-changes-using-repo)