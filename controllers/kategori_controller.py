from database.db import get_session
from models.kategori import Kategori
from sqlalchemy.orm import selectinload


class KategoriController:
    """Controller untuk operasi CRUD Kategori."""

    def semua_kategori(self):
        session = get_session()
        try:
            return (
                session.query(Kategori)
                .options(selectinload(Kategori.daftar_produk))
                .order_by(Kategori.nama.asc())
                .all()
            )
        finally:
            session.close()

    def ambil_kategori(self, kategori_id):
        session = get_session()
        try:
            return (
                session.query(Kategori)
                .options(selectinload(Kategori.daftar_produk))
                .filter(Kategori.id == int(kategori_id))
                .first()
            )
        finally:
            session.close()

    def tambah_kategori(self, nama):
        nama = (nama or "").strip()
        if not nama:
            raise ValueError("Nama kategori tidak boleh kosong.")

        session = get_session()
        try:
            existing = session.query(Kategori).filter(Kategori.nama == nama).first()
            if existing:
                raise ValueError(f"Kategori '{nama}' sudah ada.")
            kat = Kategori(nama=nama)
            session.add(kat)
            session.commit()
            return kat.id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def ubah_kategori(self, kategori_id, nama):
        nama = (nama or "").strip()
        if not nama:
            raise ValueError("Nama kategori tidak boleh kosong.")

        session = get_session()
        try:
            kat = session.query(Kategori).filter(Kategori.id == int(kategori_id)).first()
            if not kat:
                raise ValueError("Kategori tidak ditemukan.")
            kat.nama = nama
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def hapus_kategori(self, kategori_id):
        session = get_session()
        try:
            kat = session.query(Kategori).filter(Kategori.id == int(kategori_id)).first()
            if not kat:
                raise ValueError("Kategori tidak ditemukan.")
            session.delete(kat)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
