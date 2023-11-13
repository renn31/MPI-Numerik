# MPI-NUMERIK
mengeksekusi program numerik secara paralel menggunakan MPI

## Device Dan Tools Yang di gunakan dalam mengeksekusi
1.	Linux Mint
  -	Linux mint master
  -	Linux mint slave1
  -	Linux mint slave2
  -	Linux mint salve3
2.	MPI (Master dan Slave)
3.	SSH (Master dan Slave)
4.	Codingan Bubble Short python

## Topology : 

![image](https://github.com/renn31/MPI-bubble-sort/assets/128461789/75118ea2-a078-42ba-a95e-d0f9d10661f1)
Pada percobaan ini digunakan empat komputer, dimana salah satunya sebagai komputer master, yang bertanggung jawab untuk mengoordinasikan dan mengontrol seluruh proses. Sementara itu, tiga komputer lainnya dijadikan sebagai slave, dengan tugas untuk menjalankan perintah-perintah dari komputer master. Penting untuk memastikan bahwa keempat komputer ini sudah terintegrasi dalam satu jaringan yang sama.	

## Konfigurasi file /etc/hosts

Lakukan pada master dan slave:

Edit file /etc/hosts melalui nano. Tambahkan isinya dengan beberapa IP dan aliasnya. Di bawah ini sebagai contoh. sesuaikan IP nya dengan komputer masing-masing. Untuk mengecek IP gunakan perintah ifconfig.

Tambahkan baris berikut dengan format :
```bash
[IP_address1] [hostname1]
[IP_address2] [hostname2] 
[IP_address3] [hostname3] 
[IP_address4] [hostname4] 
```

sesuaikan dengan komputer yang akan dijalankan, contoh:

```bash
[10.8.141.217] [master]
[10.8.143.246] [slave1] 
[10.8.143.239] [slave2] 
[10.8.143.46] [slave3]
```
#Buat User Baru

lakukan di master dan slave:

Buat user baru di master dan slave dengan perintah berikut: contohnya akan membuat user dengan nama mpiusr. Nama user harus sama pada kompuer master dan slave.

```bash
Sudo adduser <mpiusr>
````
jadikan mpiusr memiliki hak akses superuser

```bash
Sudo usermod –aG sudo mpiusr
```

masuk ke user
```bash
su – mpiusr
```

#Konfigurasi SSH

lakukan di master dan slave:
```bash
sudo apt install openssh-server
```
Perintah tersebut akan menginstal perangkat lunak OpenSSH Server pada sistem agar dapat menggunakan layanan SSH untuk mengakses dan mengelola sistem secara remote dengan aman.

lakukan di master:
```bash
ssh-keygen -t rsa
```
Perintah ini akan membuat kunci SSH baru. Lewatkan seluruh input. Setelah melalui tahap tersebut akan ada folder .ssh dan di dalamnya terdapat file id_rsa dan id_rsa.pub.

Salin isi dari file id_rsa.pubke file authorized_keyske semua slave menggunakan perintah berikut:
```bash
cd .ssh
cat id_rsa.pub | ssh <nama user>@<host> "mkdir .ssh; cat >> .ssh/authorized_keys"
```
Lakukan penyalinan perintah berulang-ulang dari master ke slave dengan mengubah <host>  menjadi nama host masing-masing slave. Dengan membagikan kunci SSH, master akan dapat mengakses server slave jarak jauh dengan aman tanpa perlu memasukkan kata sandi setiap kali.

## konfigurasi NFS

Lakukan di master dan slave:

•	Buat shared folder

```bash
mkdir fix
```

lakukan di master:

•	Install NFS Server
```bash
sudo apt install nfs-kernel-server
```
Perintah ini akan menginstall paket nfs-kernel-server pada master agar dapat berbagi direktori atau sistem berkas dengan slave.

•	Konfigurasi file /etc/exports

Edit file /etc/exports dengan editornano sudonano /etc/exports.

tambahkan baris berikut:
```bash
<lokasi shared folder> *(rw,sync,no_root_squash,no_subtree_check)
```
Sesuaikan<lokasi shared folder>denganlokasi folder yg telah dibuat:
```bash
/home/mpiusr/fix *(rw,sync,no_root_squash,no_subtree_check)
```
Lakukan perintah berikut untuk memastikan bahwa perubahan konfigurasi yang dilakukan dalam file /etc/exports diterapkan tanpa harus memulai ulang layanan NFS.
```bash
Sudo exportfs –a
```
Jalankan perintah ini untuk memuat ulang layanan server NFS dan menerapkan perubahan konfigurasi terbaru dalam file konfigurasi /etc/exports.

```bash
Sudo systemctl restart nfs-kernel-server
```

lakukan di slave:

•	Install NFS 
```bash
sudo apt install nfs-common
```
Paket nfs-common akan di install, memungkinkan untuk mengakses dan menggunakan berkas yang dibagikan oleh master NFS yang telah dikonfigurasi dengan benar.

•	lakukan mounting dengan perintah berikut:

```bash
sudo mount <server host>:<lokasi shared folder di master><lokasi shared folder di slave>
```
sesuaikan <server host>, <lokasi shared folder di master> dan<lokasi shared folder di slave>. contohnya:
```bash
sudo mount master:/home/mpiusr/fix /home/mpiusr/fix
```

## MPI

lakukan di master dan slave:

•	install mpi dengan perintah beriku
```bash
sudo apt install openmpi-bin libopenmpi-dev
```

•	lakukan testing untuk pengeksekusian
lakukan di master:

Buat file python di folder fix. Misal test.py
```bash
touch test.py
```
Kemudian edit file menggunakan perintah nano dengan mengisi file tersebut dengan perogram python sederhana, misalnya:
```bash
Print("Selamat Datang Linux Lover <3")
```
Gunakan perintah berikut untuk mengeksekusi program tersebut:
```bash
mpirun -np <jumlahprosesor> -host <daftar host> python3 test.py
```
Sesuaikan dengan progrm yang akan dijalankan
```bash
mpirun -np 3 -host master,slave1,slave2,slave3 python3 test.py
```

##Eksekusi program Numerik dengan MPI

lakukan di master:
```bash
sudo apt install python3-pip
pip install mpi4py
```

lakukan di maser:

Buat program dengan metode numerik menggunakan bahasa pemrograman python.
```bash
nano pers22.py
```
isi pers22.py dengan program numerik contohnya untuk menghitung akar-akar dari persamaan kuadrat seperti pada program berikut ini:

```bash
from mpi4py import MPI
import math

# Inisialisasi MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Input koefisien a, b, dan c dari proses 0
a = None
b = None
c = None

if rank == 0:
    a = float(input("Masukkan koefisien a: "))
    b = float(input("Masukkan koefisien b: "))
    c = float(input("Masukkan koefisien c: "))

# Broadcast koefisien a, b, dan c dari proses 0 ke semua proses
a = comm.bcast(a, root=0)
b = comm.bcast(b, root=0)
c = comm.bcast(c, root=0)

# Hitung diskriminan di semua proses
diskriminan = b**2 - 4*a*c
# Inisialisasi variabel untuk menerima hasil
x1 = None
x2 = None

# Cek apakah diskriminan positif, nol, atau negatif di semua proses
if diskriminan > 0:
    x1_local = (-b + math.sqrt(diskriminan)) / (2*a)
    x2_local = (-b - math.sqrt(diskriminan)) / (2*a)
elif diskriminan == 0:
    x1_local = -b / (2*a)
    x2_local = x1_local
else:
    realPart = -b / (2*a)
    imaginaryPart = math.sqrt(-diskriminan) / (2*a)
    x1_local = complex(realPart, imaginaryPart)
    x2_local = complex(realPart, -imaginaryPart)

# Kumpulkan hasil dari semua proses ke proses 0
x1 = comm.gather(x1_local, root=0)
x2 = comm.gather(x2_local, root=0)

# Di proses 0, cetak hasil akar-akar persamaan kuadrat
if rank == 0:
    print("Akar-akar persamaan kuadrat adalah:")
    for i in range(size):
        print(f"Proses {i}:")
        print("x1 =", x1[i])
        print("x2 =", x2[i])
```

Gunakan perintah berikut untuk mengeksekusi program tersebut:
```bash
mpirun -np <jumlahprosesor> -host <daftar host> python3 pers22.py
```
Sesuaikan dengan progrm yang akan dijalankan:
```bash
mpirun -np 3 -host master, slave1,slave2,slave3  python3 pers22.py
```

