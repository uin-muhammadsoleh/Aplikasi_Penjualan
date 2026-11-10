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
        nama = (nama or "").strip()
        if not nama:
            raise ValueError("Nama produk wajib diisi.")
        if harga < 0 or stok < 0:
            raise ValueError("Harga dan stok tidak boleh negatif.")

        session = get_session()
        try:
            kat_id = int(kategori_id) if kategori_id else None
            produk = Produk(
                nama=nama,
                harga=float(harga),
                stok=int(stok),
                kategori_id=kat_id,
            )
            session.add(produk)
            session.commit()
            return produk.id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def ubah_produk(self, produk_id, nama, harga, stok, kategori_id=None):
        nama = (nama or "").strip()
        if not nama:
            raise ValueError("Nama produk wajib diisi.")
        if harga < 0 or stok < 0:
            raise ValueError("Harga dan stok tidak boleh negatif.")

        session = get_session()
        try:
            produk = session.query(Produk).filter(Produk.id == int(produk_id)).first()
            if produk is None:
                raise ValueError("Produk tidak ditemukan.")
            produk.nama = nama
            produk.harga = float(harga)
            produk.stok = int(stok)
            produk.kategori_id = int(kategori_id) if kategori_id else None
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
