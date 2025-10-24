import pytest

from online_course.exceptions import (
    PendidikanTidakMemenuhiSyaratError,
    UsiaTidakMemenuhiSyaratError,
)
from online_course.kursus import KursusOnline
from online_course.peserta import Peserta
from online_course.main import process_registration


# ---------- Konstruktor Peserta ----------

def test_peserta_init_valid():
    p = Peserta("Rina", 20, "Sarjana")
    assert p.get_nama() == "Rina"
    assert p.get_usia() == 20
    assert p.get_tingkat_pendidikan() == "Sarjana"


@pytest.mark.parametrize("nama", ["", "   ", None])
def test_peserta_init_nama_invalid(nama):
    with pytest.raises(ValueError):
        Peserta(nama, 20, "Sarjana")


def test_peserta_init_usia_bukan_int():
    with pytest.raises(ValueError):
        Peserta("Ari", "20", "Sarjana")


# ---------- cek_kelayakan ----------

def test_kelayakan_usia_kurang_dari_18():
    p = Peserta("Budi", 17, "Sarjana")
    with pytest.raises(UsiaTidakMemenuhiSyaratError) as excinfo:
        p.cek_kelayakan()
    assert "usia Anda tidak memenuhi syarat" in str(excinfo.value)


@pytest.mark.parametrize("edu", ["SMA", "Diploma", "Doktor", ""])
def test_kelayakan_pendidikan_tidak_memenuhi(edu):
    p = Peserta("Citra", 25, edu)
    with pytest.raises(PendidikanTidakMemenuhiSyaratError) as excinfo:
        p.cek_kelayakan()
    assert "tingkat pendidikan Anda tidak memenuhi syarat" in str(excinfo.value)


def test_kelayakan_lolos():
    p = Peserta("Doni", 30, "Magister")
    # tidak raise apa pun
    p.cek_kelayakan()


# ---------- KursusOnline.daftar_peserta ----------

def test_daftar_peserta_valid_bertambah():
    kursus = KursusOnline()
    p = Peserta("Eka", 21, "Sarjana")
    kursus.daftar_peserta(p)
    daftar = kursus.get_daftar_peserta()
    assert len(daftar) == 1 and daftar[0] is p


def test_daftar_peserta_gagal_usia():
    kursus = KursusOnline()
    p = Peserta("Feri", 10, "Sarjana")
    with pytest.raises(UsiaTidakMemenuhiSyaratError):
        kursus.daftar_peserta(p)
    assert len(kursus.get_daftar_peserta()) == 0


def test_daftar_peserta_gagal_pendidikan():
    kursus = KursusOnline()
    p = Peserta("Gita", 22, "SMA")
    with pytest.raises(PendidikanTidakMemenuhiSyaratError):
        kursus.daftar_peserta(p)
    assert len(kursus.get_daftar_peserta()) == 0


# ---------- process_registration: memastikan finally selalu jalan ----------

def test_process_registration_menampilkan_pesan_finally_saat_sukses(capsys):
    kursus = KursusOnline()
    p = Peserta("Hana", 23, "Sarjana")
    process_registration(kursus, p)
    out = capsys.readouterr().out
    assert "Pendaftaran berhasil: Hana" in out
    assert "Proses pendaftaran selesai." in out


def test_process_registration_menampilkan_pesan_finally_saat_gagal_usia(capsys):
    kursus = KursusOnline()
    p = Peserta("Imam", 16, "Sarjana")
    process_registration(kursus, p)
    out = capsys.readouterr().out
    assert "Gagal daftar (Imam)" in out
    assert "usia Anda tidak memenuhi syarat" in out
    assert "Proses pendaftaran selesai." in out


def test_process_registration_menampilkan_pesan_finally_saat_gagal_pendidikan(capsys):
    kursus = KursusOnline()
    p = Peserta("Joko", 25, "SMA")
    process_registration(kursus, p)
    out = capsys.readouterr().out
    assert "Gagal daftar (Joko)" in out
    assert "tingkat pendidikan Anda tidak memenuhi syarat" in out
    assert "Proses pendaftaran selesai." in out
