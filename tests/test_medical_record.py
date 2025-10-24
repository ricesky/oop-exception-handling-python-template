import pytest

from medical_record.exceptions import DataTidakLengkapError, DataTidakValidError
from medical_record.pasien import Pasien
from medical_record.pemeriksaan import Pemeriksaan


# ---------- Pasien.validasi_data ----------

def test_validasi_data_lolos():
    p = Pasien("Rina", 28, "Jl. Kenanga")
    # Tidak raise
    p.validasi_data()


@pytest.mark.parametrize(
    "nama, umur, alamat",
    [
        ("", 25, "Jl. Mawar"),
        ("   ", 25, "Jl. Mawar"),
        ("Budi", 25, ""),
        ("Budi", 25, "   "),
    ],
)
def test_validasi_data_tidak_lengkap(nama, umur, alamat):
    p = Pasien(nama, umur, alamat)
    with pytest.raises(DataTidakLengkapError) as excinfo:
        p.validasi_data()
    assert "Data pasien tidak lengkap." in str(excinfo.value)


@pytest.mark.parametrize("umur", [-1, -10, 121, 999])
def test_validasi_data_tidak_valid_umur(umur):
    p = Pasien("Ari", umur, "Jl. Melati")
    with pytest.raises(DataTidakValidError) as excinfo:
        p.validasi_data()
    assert "Data yang dimasukkan tidak valid." in str(excinfo.value)


# ---------- Pemeriksaan.periksa_data (rethrow + chaining) ----------

def test_periksa_data_ok_mengembalikan_string():
    pemeriksaan = Pemeriksaan()
    p = Pasien("Cici", 30, "Jl. Anggrek")
    assert pemeriksaan.periksa_data(p) == "Data pasien valid"


@pytest.mark.parametrize(
    "nama, umur, alamat, expected_msg",
    [
        ("", 30, "Jl. Melati", "Validasi gagal: nama/alamat kosong."),
        ("   ", 30, "Jl. Melati", "Validasi gagal: nama/alamat kosong."),
        ("Doni", 30, "", "Validasi gagal: nama/alamat kosong."),
        ("Doni", 30, "   ", "Validasi gagal: nama/alamat kosong."),
    ],
)
def test_periksa_data_rethrow_lengkap_memperbarui_pesan_dan_chaining(nama, umur, alamat, expected_msg):
    pemeriksaan = Pemeriksaan()
    p = Pasien(nama, umur, alamat)
    with pytest.raises(DataTidakLengkapError) as excinfo:
        pemeriksaan.periksa_data(p)

    # Pesan diperbarui
    err = excinfo.value
    assert expected_msg in str(err)

    # Chaining aktif (sebab asli ada dan bertipe sama)
    assert err.__cause__ is not None
    assert isinstance(err.__cause__, DataTidakLengkapError)
    assert "Data pasien tidak lengkap." in str(err.__cause__)


@pytest.mark.parametrize("umur", [-5, 130])
def test_periksa_data_rethrow_valid_memperbarui_pesan_dan_chaining(umur):
    pemeriksaan = Pemeriksaan()
    p = Pasien("Eka", umur, "Jl. Dahlia")

    with pytest.raises(DataTidakValidError) as excinfo:
        pemeriksaan.periksa_data(p)

    err = excinfo.value
    assert "Validasi gagal: umur di luar rentang 0–120." in str(err)

    assert err.__cause__ is not None
    assert isinstance(err.__cause__, DataTidakValidError)
    assert "Data yang dimasukkan tidak valid." in str(err.__cause__)
