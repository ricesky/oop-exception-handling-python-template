import pytest

from ticket_booking.exceptions import (
    KapasitasPenuhError,
    NomorTiketTidakDitemukanError,
    TiketSudahDipesanError,
)
from ticket_booking.penumpang import Penumpang
from ticket_booking.pemesanan import PemesananTiket
from ticket_booking.main import process_booking


# ---------- Konstruktor & Validasi ----------
def test_init_kapasitas_valid():
    s = PemesananTiket(3)
    assert s.get_kapasitas() == 3
    assert s.get_jumlah_terpesan() == 0


@pytest.mark.parametrize("kapasitas", [0, -1, "3"])
def test_init_kapasitas_invalid(kapasitas):
    with pytest.raises(ValueError):
        PemesananTiket(kapasitas)


# ---------- Penumpang ----------
def test_penumpang_init_valid():
    p = Penumpang("Rina", "ID001")
    assert p.get_nama() == "Rina"
    assert p.get_identitas() == "ID001"


@pytest.mark.parametrize(
    "nama, identitas",
    [
        ("", "ID001"),
        ("   ", "ID001"),
        (None, "ID001"),
        ("Rina", ""),
        ("Rina", "   "),
        ("Rina", None),
    ],
)
def test_penumpang_init_invalid(nama, identitas):
    with pytest.raises(ValueError):
        Penumpang(nama, identitas)


# ---------- PemesananTiket: pesan_tiket ----------
def test_pesan_tiket_sukses_menambah_data():
    s = PemesananTiket(2)
    p = Penumpang("Ayu", "ID001")
    s.pesan_tiket("T-001", p)
    assert s.get_jumlah_terpesan() == 1
    assert s.ada_tiket("T-001") is True


def test_pesan_tiket_duplikat_menimbulkan_error():
    s = PemesananTiket(2)
    p1 = Penumpang("Ayu", "ID001")
    p2 = Penumpang("Budi", "ID002")
    s.pesan_tiket("T-001", p1)
    with pytest.raises(TiketSudahDipesanError):
        s.pesan_tiket("T-001", p2)  # nomor tiket sama


def test_pesan_tiket_kapasitas_penuh():
    s = PemesananTiket(2)
    s.pesan_tiket("T-001", Penumpang("Ayu", "ID001"))
    s.pesan_tiket("T-002", Penumpang("Budi", "ID002"))
    with pytest.raises(KapasitasPenuhError):
        s.pesan_tiket("T-003", Penumpang("Cici", "ID003"))


@pytest.mark.parametrize("nomor", ["", "   ", None])
def test_pesan_tiket_nomor_kosong_invalid(nomor):
    s = PemesananTiket(1)
    with pytest.raises(ValueError):
        s.pesan_tiket(nomor, Penumpang("Ayu", "ID001"))


# ---------- PemesananTiket: batalkan_tiket ----------
def test_batalkan_tiket_sukses_mengurangi_data():
    s = PemesananTiket(2)
    s.pesan_tiket("T-001", Penumpang("Ayu", "ID001"))
    assert s.get_jumlah_terpesan() == 1
    s.batalkan_tiket("T-001")
    assert s.get_jumlah_terpesan() == 0
    assert s.ada_tiket("T-001") is False


def test_batalkan_tiket_nomor_tidak_ditemukan():
    s = PemesananTiket(2)
    with pytest.raises(NomorTiketTidakDitemukanError):
        s.batalkan_tiket("T-XYZ")


# ---------- process_booking (pastikan finally selalu dieksekusi) ----------
def test_process_booking_sukses_mencetak_ringkasan(capsys):
    s = PemesananTiket(1)
    p = Penumpang("Ayu", "ID001")
    process_booking(s, "T-001", p)
    out = capsys.readouterr().out
    assert "Pesan tiket berhasil: T-001" in out
    assert "Jumlah tiket terpesan: 1 dari 1" in out
    assert "Proses pemesanan selesai." in out


def test_process_booking_kapasitas_penuh_mencetak_ringkasan(capsys):
    s = PemesananTiket(1)
    s.pesan_tiket("T-001", Penumpang("Ayu", "ID001"))
    process_booking(s, "T-002", Penumpang("Budi", "ID002"))
    out = capsys.readouterr().out
    assert "Gagal pesan (T-002)" in out
    assert "Kursi sudah penuh" in out
    assert "Jumlah tiket terpesan: 1 dari 1" in out
    assert "Proses pemesanan selesai." in out


def test_process_booking_duplikat_mencetak_ringkasan(capsys):
    s = PemesananTiket(2)
    s.pesan_tiket("T-001", Penumpang("Ayu", "ID001"))
    process_booking(s, "T-001", Penumpang("Budi", "ID002"))
    out = capsys.readouterr().out
    assert "Gagal pesan (T-001)" in out
    assert "sudah dipesan" in out
    assert "Jumlah tiket terpesan: 1 dari 2" in out
    assert "Proses pemesanan selesai." in out
