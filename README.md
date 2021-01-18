# SIMAK EPBM

Program ini dibuat agar memudahkan programer mengisi simak.

Terdiri dari 2 file penting yaitu :

- main.py
- model/robot.py

Package yang harus ada :

- python-dotenv
- requests
- BeutifulSoup

Versi python yang digunakan `python 3.6.8`

# CARA PEMAKAIAN

Copy file `.env.backup` ke file `.env` dan isi dengan username serta password akun IPB kalian :

```
USERNAME_IPB=blablabla
PASSWORD_IPB=blablabla
```

Buka terminal atau command line yang sudah terinstall python:

```python
python --version
Python 3.6.8 # atau diatasnya
```

Pindah ke folder project ini, lalu jalankan dengan:

```python
python main.py
```

Output yang keluar kira-kira akan seperti ini:

```
Beep boop ! robot untuk {username_kalian} siap
Mencoba melakukan GET ke alamat : https://simak.ipb.ac.id/Account/Login
Beep boop ! sekarang anda berada di https://simak.ipb.ac.id/Account/Login
Mencoba melakukan POST_LOGIN ke alamat : https://simak.ipb.ac.id/Account/Login
Beep boop ! berhasil login
Mencoba melakukan GET ke alamat : https://simak.ipb.ac.id/Home
Beep boop ! sekarang anda berada di https://simak.ipb.ac.id/Home
Memberikan hasil pencarian menu sidebar:
Halaman : Beranda (https://simak.ipb.ac.id/Home/Index)
Halaman : Biodata (https://simak.ipb.ac.id/MenuMahasiswa/Biodata)
Halaman : Pemilihan Minor (https://simak.ipb.ac.id/KRSSarjana/Minor/Index)
Halaman : Pengisian Form Perwalian (https://simak.ipb.ac.id/KRSSarjana/Perwalian)
Halaman : KRS (https://simak.ipb.ac.id/KRSSarjana/KRSOnline/RencanaStudi)
Halaman : EPBM (https://simak.ipb.ac.id/EPBMOnline/EPBM/Index)
Halaman : Jadwal Saya (https://simak.ipb.ac.id/KRSSarjana/JadwalSaya)
Halaman : Daftar Hadir (https://simak.ipb.ac.id/MenuMahasiswa/KehadiranMahasiswa)
Halaman : Rekapitulasi Studi (https://simak.ipb.ac.id/RekapitulasiStudi/Index)
Halaman : Jadwal Departemen (https://simak.ipb.ac.id/KRSSarjana/JadwalDepartemen)
Halaman : Pembayaran SPP (https://simak.ipb.ac.id/MenuMahasiswa/BiayaPendidikan)
Halaman : Pendaftaran Wisuda (https://simak.ipb.ac.id/Wisuda/PendaftaranWisuda/Index)
Halaman : PPKI (https://simak.ipb.ac.id/MenuMahasiswa/DokumenPPKI)
Halaman : Pengisian Form SKW (https://simak.ipb.ac.id/Wisuda/SKW/Index)
Mencoba melakukan GET ke alamat : https://simak.ipb.ac.id/EPBMOnline/EPBM/Index
Beep boop ! sekarang anda berada di https://simak.ipb.ac.id/EPBMOnline/EPBM/Index
...
...
...
Beep boop ! sekarang anda berada di https://simak.ipb.ac.id/EPBMOnline/EPBM/Detail/7201?t=48
Memberikan hasil matakuliah yang belum diisi EPBM nya :
[<font size="6">KOM330</font>]
KOM330: https://simak.ipb.ac.id/EPBMOnline/EPBM/FormEPBM/5116420?p=7201
[<font size="6">KOM398</font>]
KOM398: https://simak.ipb.ac.id/EPBMOnline/EPBM/FormEPBM/5117237?p=7201
[<font size="6">KOM302</font>]
KOM302: https://simak.ipb.ac.id/EPBMOnline/EPBM/FormEPBM/5121750?p=7201
[<font size="6">FMP400</font>]
FMP400: https://simak.ipb.ac.id/EPBMOnline/EPBM/FormEPBM/5128770?p=7201
[<font size="6">IKK335</font>]
IKK335: https://simak.ipb.ac.id/EPBMOnline/EPBM/FormEPBM/5182350?p=7201
[<font size="6">IKK214</font>]
IKK214: https://simak.ipb.ac.id/EPBMOnline/EPBM/FormEPBM/5184494?p=7201
Beep boop ! apa anda yakin mengisi epbm KOM330 ? (y/n)
...
...
...
```

Tekan `y` lalu enter untuk mengisi epbm secara otomatis, selain itu tekan `n` jika tidak ingin mengisi epbm.

```
Drrt drrt ! EPBM berhasil disimpan.
```

Akan muncul tulisan seperti di atas jika epbm berhasil disimpan.

# PENTING

Saat program run dan mulai mengisi epbm, kalian harus menginput/mengetik 'y' untuk yes (mulai mengisi epbm tertentu)
atau 'n' untuk no (membatalkan mengisi epbm tertentu).

# TESTED

![Gambar Testing](pict/tested.png)
