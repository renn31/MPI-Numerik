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