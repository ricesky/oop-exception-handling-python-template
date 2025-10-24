# tests/test_bank_account.py
import pytest

from bank_account.bank import Bank
from bank_account.rekening import Rekening
from bank_account.exceptions import (
    SaldoTidakCukupError,
    RekeningTidakDitemukanError,
    BatasPenarikanError,
)

# ---------- Inisialisasi & Validasi Rekening ----------

def test_rekening_init_valid():
    r = Rekening("001", 150_000)
    assert r.get_nomor() == "001"
    assert r.get_saldo() == 150_000.0

@pytest.mark.parametrize("nomor", ["", "   ", None])
def test_rekening_init_nomor_invalid(nomor):
    with pytest.raises(ValueError):
        Rekening(nomor, 0)

@pytest.mark.parametrize("saldo_awal", [-1, -0.01, -10_000])
def test_rekening_init_saldo_awal_negatif(saldo_awal):
    with pytest.raises(ValueError):
        Rekening("001", saldo_awal)

# ---------- Validasi Input Penarikan ----------

@pytest.mark.parametrize("jumlah", [None, "abc"])
def test_penarikan_jumlah_bukan_angka(jumlah):
    r = Rekening("001", 100_000)
    with pytest.raises(ValueError) as excinfo:
        r.penarikan(jumlah)
    assert "harus berupa angka" in str(excinfo.value)

@pytest.mark.parametrize("jumlah", [0, -1, -1000])
def test_penarikan_jumlah_tidak_positif(jumlah):
    r = Rekening("001", 100_000)
    with pytest.raises(ValueError) as excinfo:
        r.penarikan(jumlah)
    assert "harus > 0" in str(excinfo.value)

# ---------- Batas Penarikan Harian ----------

def test_penarikan_melebihi_batas_harian():
    r = Rekening("001", 200_000)
    # > 100_000 (BATAS_PENARIKAN_HARIAN)
    with pytest.raises(BatasPenarikanError):
        r.penarikan(100_001)

def test_penarikan_sama_dengan_batas_harian_diperbolehkan_jika_saldo_cukup():
    r = Rekening("001", 150_000)
    r.penarikan(Rkening := Rekening.BATAS_PENARIKAN_HARIAN)  # 100_000
    assert r.get_saldo() == 50_000.0

# ---------- Saldo Tidak Cukup ----------

def test_penarikan_saldo_tidak_cukup():
    r = Rekening("001", 50_000)
    with pytest.raises(SaldoTidakCukupError):
        r.penarikan(75_000)

# ---------- Penarikan Berhasil Mengurangi Saldo ----------

def test_penarikan_valid_mengurangi_saldo():
    r = Rekening("001", 120_000)
    r.penarikan(25_000)
    assert r.get_saldo() == 95_000.0
    r.penarikan(95_000)
    assert r.get_saldo() == 0.0

# ---------- Bank: Tambah & Cari Rekening ----------

def test_bank_tambah_dan_cari_rekening():
    bank = Bank()
    r1 = Rekening("001", 10_000)
    r2 = Rekening("002", 20_000)

    bank.tambah_rekening(r1)
    bank.tambah_rekening(r2)

    assert bank.cari_rekening("001") is r1
    assert bank.cari_rekening("002") is r2

def test_bank_tambah_rekening_duplikat():
    bank = Bank()
    r = Rekening("001", 10_000)
    bank.tambah_rekening(r)
    with pytest.raises(ValueError):
        bank.tambah_rekening(Rekening("001", 5_000))  # nomor duplikat

def test_bank_cari_rekening_tidak_ditemukan():
    bank = Bank()
    bank.tambah_rekening(Rekening("001", 10_000))
    with pytest.raises(RekeningTidakDitemukanError):
        bank.cari_rekening("999")

# ---------- Integrasi: Skenario Campuran ----------

def test_integrasi_skenario_campuran():
    bank = Bank()
    r1 = Rekening("001", 150_000)
    r2 = Rekening("002", 50_000)
    bank.tambah_rekening(r1)
    bank.tambah_rekening(r2)

    # penarikan valid
    bank.cari_rekening("001").penarikan(25_000)
    assert bank.cari_rekening("001").get_saldo() == 125_000.0

    # melebihi batas harian
    with pytest.raises(BatasPenarikanError):
        bank.cari_rekening("001").penarikan(150_000)

    # saldo tidak cukup
    with pytest.raises(SaldoTidakCukupError):
        bank.cari_rekening("002").penarikan(75_000)

    # rekening tak ada
    with pytest.raises(RekeningTidakDitemukanError):
        bank.cari_rekening("ABC")
