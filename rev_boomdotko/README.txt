The trick with this challenge is first finding the sysfs_store function within the kernel module.
In that function there were calls to prepare_creds and commit_creds. The string that gets put in there
is visible in the binary, with some XOR stuff included to obfuscate it. That comes out to 1337p4ssw0rd7331.
Then, after spawning the docker, you can nc to the IP, and you will get a non-elevated terminal session.
When you echo the password into the kernel module (by using /sys/kernel/boom/boom to write data to the kernel object) you get a root shell. And then you can cat the flag.

~ $ ls
ls
bin       etc       init      proc      sbin      tmp
dev       flag.txt  lib       root      sys
~ $ cat flag.txt
cat flag.txt
cat: can't open 'flag.txt': Permission denied
~ $ ls -altr
ls -altr
total 8
drwxr-xr-x    2 0        0               40 Feb 12  2025 tmp
drwxr-xr-x    2 0        0               40 Feb 12  2025 sbin
drwxr-xr-x    2 0        0               40 Feb 12  2025 root
drwxr-xr-x    3 0        0               60 Feb 12  2025 lib
drwxr-xr-x    2 0        0               40 Feb 12  2025 etc
drwxr-xr-x    2 0        0             8140 Feb 12  2025 bin
-r--------    1 0        0               26 Feb 12  2025 flag.txt
-rwxr-xr-x    1 0        0              164 Feb 12  2025 init
drwxr-xr-x   11 0        0              260 Feb 12  2025 ..
drwxr-xr-x   11 0        0              260 Feb 12  2025 .
dr-xr-xr-x   13 0        0                0 Nov 13 23:57 sys
dr-xr-xr-x   97 0        0                0 Nov 13 23:57 proc
drwxr-xr-x    2 0        0               80 Nov 13 23:57 dev
~ $ lsmod
lsmod
boom 16384 0 - Live 0x0000000000000000 (OE)
~ $ echo -n '1337p4ssw0rd7331' | tee /sys/kernel/boom/boom
echo -n '1337p4ssw0rd7331' | tee /sys/kernel/boom/boom
1337p4ssw0rd7331~ $ 

~ $ id
id
uid=65534 gid=65534 groups=65534
~ $ cat flag.txt
cat flag.txt
cat: can't open 'flag.txt': Permission denied
~ $ cat init
cat init
#!/bin/sh
 mount -t proc proc /proc
 mount -t sysfs sysfs /sys
 mknod /dev/ttyS0 c 4 64
 insmod /lib/modules/boom.ko
 setsid /bin/cttyhack setuidgid 65534 /bin/sh

~ $ ls /sys/kernel/boom
ls /sys/kernel/boom
boom
~ $ ls -altr /sys/kernel/boom/boom
ls -altr /sys/kernel/boom/boom
-rw-rw-rw-    1 0        0             4096 Nov 13 23:58 /sys/kernel/boom/boom
~ $ echo -n '1337p4ssw0rd7331' | /sys/kernel/boom/boom
echo -n '1337p4ssw0rd7331' | /sys/kernel/boom/boom
/bin/sh: /sys/kernel/boom/boom: Permission denied
~ $ ls          
ls
bin       etc       init      proc      sbin      tmp
dev       flag.txt  lib       root      sys
~ $ echo -n '1337p4ssw0rd7331' > /sys/kernel/boom/boom
echo -n '1337p4ssw0rd7331' > /sys/kernel/boom/boom
~ # ls
ls
bin       etc       init      proc      sbin      tmp
dev       flag.txt  lib       root      sys
~ # cat flag.txt
cat flag.txt
HTB{s3cr3ts_in_ur_k3rn3l}
~ #                                                                                                             
