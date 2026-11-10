from database.db import get_session
from models.kategori import Kategori
from models.produk import Produk
from sqlalchemy.orm import joinedload


class ProdukController:
    """Controller untuk operasi CRUD produk dengan dukungan Kategori."""

    def semua_produk(self):
        """Mengambil seluruh daftar produk berserta relasi kategorinya."""
        session = get_session()
        try:
            return (
                session.query(Produk)
                .options(joinedload(Produk.kategori))
                .order_by(Produk.id.desc())
                .all()
            )
        finally:
            session.close()

    def ambil_produk(self, produk_id):
        """Mengambil satu data produk berdasarkan ID berserta relasi kategorinya."""
        session = get_session()
        try:
            return (
                session.query(Produk)
                .options(joinedload(Produk.kategori))
                .filter(Produk.id == int(produk_id))
                .first()
            )
        finally:
            session.close()

    def semua_kategori(self):
        """Mengambil seluruh daftar kategori untuk pilihan dropdown."""
        session = get_session()
        try:
            return session.query(Kategori).order_by(Kategori.nama.asc()).all()
        finally:
            session.close()

    def tambah_produk(self, nama, harga, stok, kategori_id=None):
        """Menambahkan produk baru menggunakan setter pada model Produk untuk validasi data."""
        session = get_session()
        try:
            produk = Produk()
            # Validasi data secara otomatis dieksekusi di dalam method setter
            produk.set_nama(nama)
            produk.set_harga(harga)
            produk.set_stok(stok)
            produk.set_kategori_id(kategori_id)

            session.add(produk)
            session.commit()
            return produk.id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def ubah_produk(self, produk_id, nama, harga, stok, kategori_id=None):
        """Memperbarui data produk menggunakan setter pada model Produk untuk validasi data."""
        session = get_session()
        try:
            produk = session.query(Produk).filter(Produk.id == int(produk_id)).first()
            if produk is None:
                raise ValueError("Produk tidak ditemukan.")

            # Validasi data melalui setter
            produk.set_nama(nama)
            produk.set_harga(harga)
            produk.set_stok(stok)
            produk.set_kategori_id(kategori_id)

            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def hapus_produk(self, produk_id):
        session = get_session()
        try:
            produk = session.query(Produk).filter(Produk.id == int(produk_id)).first()
            if produk is None:
                raise ValueError("Produk tidak ditemukan.")
            session.delete(produk)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
