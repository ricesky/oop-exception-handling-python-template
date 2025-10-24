# oop-exception-handling-python

## Sub Capaian Pembelajaran

1. Mahasiswa mampu mengimplementasikan alur tidak normal menggunakan mekanisme **exception throwing** (`raise`).
2. Mahasiswa mampu mengimplementasikan penanganan error menggunakan konstruksi **`try–except`** (serta `else` dan `finally` bila diperlukan).
3. Mahasiswa mampu mengimplementasikan **custom exception** yang bermakna bagi domain masalah.
4. Mahasiswa mampu melakukan **exception chaining** untuk memperkaya konteks error (opsional namun direkomendasikan).

---

## Lingkungan Pengembangan

1. Platform: **Python 3.10+**
2. Bahasa: **Python**
3. Editor/IDE:

   * VS Code + Python Extension
   * Terminal

---

## Cara Menjalankan Project

1. Clone repositori project `oop-exception-handling-python` ke direktori lokal Anda:

   ```bash
   git clone https://github.com/USERNAME/oop-exception-handling-python.git
   cd oop-exception-handling-python
   ```
2. Buat & aktifkan virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux/macOS
   .venv\Scripts\activate           # Windows
   ```
3. Install dependensi:

   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan unit test:

   ```bash
   pytest
   ```

> **PERINGATAN:** Push ke remote **hanya jika seluruh unit test lulus** (semua hijau).

---

## Soal-soal

### Soal 1 — Pengecekan Akun Bank

**Lokasi:** `src/bank_account/`
**Namespace (modul):** `bank_account`

#### Custom Exceptions (`exceptions.py`)

Buat exception yang mewarisi `Exception`:

1. `SaldoTidakCukupError` → pesan default: `"Saldo tidak mencukupi!"`
2. `RekeningTidakDitemukanError` → pesan default: `"Rekening tidak ditemukan!"`
3. `BatasPenarikanError` → pesan default: `"Melebihi batas penarikan harian."`

> Catatan: Sediakan opsi untuk mengisi pesan kustom pada `__init__`, namun memiliki **default message** di atas.

#### Kelas `Rekening` (`rekening.py`)

* Atribut privat:

  * `_nomor: str`
  * `_saldo: float`
* Konstanta kelas: `BATAS_PENARIKAN_HARIAN = 100_000` (dalam satuan yang konsisten, mis. rupiah).
* Metode:

  * `penarikan(self, jumlah: float) -> None`

    * Validasi `jumlah > 0` (jika tidak, **raise** `ValueError("Jumlah penarikan harus > 0")`).
    * Jika `jumlah > BATAS_PENARIKAN_HARIAN` → **raise** `BatasPenarikanError`.
    * Jika `jumlah > _saldo` → **raise** `SaldoTidakCukupError`.
    * Jika valid → kurangi `_saldo`.
  * `get_saldo(self) -> float`
  * `get_nomor(self) -> str`

#### Kelas `Bank` (`bank.py`)

* Atribut:

  * `_daftar: dict[str, Rekening]` (key = nomor rekening)
* Metode:

  * `tambah_rekening(self, rek: Rekening) -> None`

    * Tolak duplikasi nomor (jika duplikat, **raise** `ValueError("Nomor rekening sudah ada")`).
  * `cari_rekening(self, nomor: str) -> Rekening`

    * Jika tidak ada, **raise** `RekeningTidakDitemukanError`.

#### Demo `main.py`

* Tambah beberapa rekening.
* Lakukan beberapa penarikan dalam blok `try–except` yang **spesifik**:

  * `SaldoTidakCukupError`
  * `BatasPenarikanError`
  * `RekeningTidakDitemukanError`
  * `Exception as e` (fallback) → hanya untuk logging.
* Cetak saldo akhir tiap rekening di blok `finally`.

**Kriteria Lulus (unit test inti):**

* Menarik di atas saldo → `SaldoTidakCukupError`.
* Menarik di atas batas harian → `BatasPenarikanError`.
* Mencari rekening tak ada → `RekeningTidakDitemukanError`.
* Penarikan valid mengubah saldo dengan benar.

---

### Soal 2 — Pendaftaran Kursus Online

**Lokasi:** `src/online_course/`
**Namespace (modul):** `online_course`

#### Custom Exceptions (`exceptions.py`)

1. `UsiaTidakMemenuhiSyaratError` → `"Maaf, usia Anda tidak memenuhi syarat untuk mengikuti kursus ini."`
2. `PendidikanTidakMemenuhiSyaratError` → `"Maaf, tingkat pendidikan Anda tidak memenuhi syarat untuk mengikuti kursus ini."`

#### Kelas `Peserta` (`peserta.py`)

* Atribut privat:

  * `_nama: str`
  * `_usia: int`
  * `_tingkat_pendidikan: str`
* Metode:

  * `cek_kelayakan(self) -> None`

    * Jika `usia < 18` → **raise** `UsiaTidakMemenuhiSyaratError`
    * Jika `tingkat_pendidikan` **bukan** salah satu dari `{"Sarjana", "Magister"}` → **raise** `PendidikanTidakMemenuhiSyaratError`

#### Kelas `KursusOnline` (`kursus.py`)

* Atribut:

  * `_peserta: list[Peserta]`
* Metode:

  * `daftar_peserta(self, peserta: Peserta) -> None`

    * Panggil `peserta.cek_kelayakan()`
    * Jika lolos → tambahkan ke daftar
  * `get_daftar_peserta(self) -> list[Peserta]`

#### Demo `main.py`

* Coba daftarkan beberapa peserta dalam loop:

  * Tangani exception menggunakan `try–except` sesuai tipe.
  * **Selalu** cetak `"Proses pendaftaran selesai."` pada blok `finally` (menandakan pendaftaran berhasil/gagal tetap menutup proses).
* Tampilkan nama peserta yang berhasil mendaftar di akhir.

**Kriteria Lulus (unit test inti):**

* Usia < 18 → `UsiaTidakMemenuhiSyaratError`.
* Pendidikan tidak termasuk ketentuan → `PendidikanTidakMemenuhiSyaratError`.
* Peserta valid masuk ke daftar.
* `finally` dieksekusi (bisa dites via *spy* pada `stdout` atau flag internal).

---

### Soal 3 — Pemeriksaan Data Pasien

**Lokasi:** `src/medical_record/`
**Namespace (modul):** `medical_record`

#### Custom Exceptions (`exceptions.py`)

1. `DataTidakLengkapError` → `"Data pasien tidak lengkap."`
2. `DataTidakValidError` → `"Data yang dimasukkan tidak valid."`

#### Kelas `Pasien` (`pasien.py`)

* Atribut:

  * `_nama: str`
  * `_umur: int`
  * `_alamat: str`
* Metode:

  * `validasi_data(self) -> None`

    * Jika `nama.strip() == ""` atau `alamat.strip() == ""` → **raise** `DataTidakLengkapError`
    * Jika `umur < 0` atau `umur > 120` → **raise** `DataTidakValidError`

#### Kelas `Pemeriksaan` (`pemeriksaan.py`)

* Metode:

  * `periksa_data(self, pasien: Pasien) -> str`

    * Gunakan `try` memanggil `pasien.validasi_data()`
    * Jika terjadi exception:

      * **Tangkap** `DataTidakLengkapError` atau `DataTidakValidError`
      * **Rethrow** (melempar ulang) dengan pesan yang lebih spesifik, **gunakan chaining**:

        * Contoh:

          ```python
          except DataTidakLengkapError as e:
              raise DataTidakLengkapError("Validasi gagal: nama/alamat kosong.") from e
          ```
    * Jika lolos, kembalikan string ringkas status, mis. `"Data pasien valid"`

#### Demo `main.py`

* Buat beberapa instans `Pasien` (valid & tidak valid).
* Panggil `Pemeriksaan.periksa_data()` dalam `try–except`:

  * Cetak pesan error spesifik dari hasil rethrow.
  * Tunjukkan perbedaan pesan asli vs pesan baru (bisa log `__cause__`).

**Kriteria Lulus (unit test inti):**

* Nama/alamat kosong → `DataTidakLengkapError` dengan pesan diperbarui (cek `str(e)`).
* Umur di luar rentang → `DataTidakValidError` dengan pesan diperbarui.
* Chaining menautkan penyebab (`e.__cause__` bukan `None`).
* Pasien valid → mengembalikan `"Data pasien valid"`.

---

## Soal 4 — Sistem Pemesanan Tiket

**Lokasi:** `src/ticket_booking/`
**Namespace (modul):** `ticket_booking`

### Custom Exceptions (`exceptions.py`)

1. `KapasitasPenuhError` → `"Kursi sudah penuh, tidak dapat memproses pemesanan."`
2. `TiketSudahDipesanError` → `"Tiket untuk penumpang ini sudah dipesan."`
3. `NomorTiketTidakDitemukanError` → `"Nomor tiket tidak ditemukan dalam sistem."`

Semua turunan dari `Exception`.

---

### Kelas `Penumpang` (`penumpang.py`)

* Atribut privat:

  * `_nama: str`
  * `_nomor_identitas: str`
* Metode:

  * `get_identitas(self) -> str`
  * `get_nama(self) -> str`

---

### Kelas `PemesananTiket` (`pemesanan.py`)

* Atribut:

  * `_kapasitas: int`
  * `_data_tiket: dict[str, Penumpang]` (key = `nomor_tiket`)
* Metode:

  * `__init__(self, kapasitas: int)` → inisialisasi dictionary kosong.
  * `pesan_tiket(self, nomor_tiket: str, penumpang: Penumpang) -> None`

    * Jika jumlah tiket sudah mencapai kapasitas → **raise** `KapasitasPenuhError`.
    * Jika `nomor_tiket` sudah ada → **raise** `TiketSudahDipesanError`.
    * Jika valid → tambahkan ke `_data_tiket`.
  * `batalkan_tiket(self, nomor_tiket: str) -> None`

    * Jika nomor tidak ditemukan → **raise** `NomorTiketTidakDitemukanError`.
    * Jika ditemukan → hapus tiket dari dictionary.
  * `get_jumlah_terpesan(self) -> int`
  * `get_kapasitas(self) -> int`

---

### Demo `main.py`

* Buat instance `PemesananTiket(kapasitas=3)`.
* Coba lakukan beberapa pemesanan:

  1. Berhasil menambah 3 penumpang.
  2. Pesanan ke-4 → `KapasitasPenuhError`.
  3. Ulangi pemesanan dengan nomor tiket sama → `TiketSudahDipesanError`.
* Tangani semua exception spesifik dengan `try–except`.
* Gunakan `finally` untuk mencetak ringkasan:

  ```
  Jumlah tiket terpesan: X dari Y
  Proses pemesanan selesai.
  ```

**Fokus:** kombinasi validasi, exception spesifik, cleanup/reporting dengan `finally`.

**Kriteria Lulus (unit test inti):**

* Kapasitas melebihi → `KapasitasPenuhError`.
* Tiket duplikat → `TiketSudahDipesanError`.
* Pembatalan tiket salah → `NomorTiketTidakDitemukanError`.
* Pemesanan valid menambah entri.

---

## Soal 5 — Extra: Merancang Sendiri

**Lokasi:** `src/extra/extra.py`

Mahasiswa diminta membuat studi kasus **sendiri** menggunakan prinsip exception handling Python yang telah dipelajari.

### Ketentuan

1. Minimal **2 custom exception**.
2. Harus menggunakan **try–except** dan **raise**.
3. Salah satu fungsi harus menggunakan **raise ... from e** (chaining).
4. Harus ada **demo** dengan output error yang jelas & blok `finally` yang menunjukkan bahwa program tetap berakhir normal.
5. Buat file `extra.py` berisi seluruh implementasi dan contoh demo:

   ```python
   if __name__ == "__main__":
       # buat beberapa skenario error dan tangani
   ```

---

=== Selesai ===
