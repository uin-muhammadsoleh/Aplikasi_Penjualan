from database.db import get_session
from models.pelanggan import Pelanggan
from sqlalchemy.orm import selectinload


class PelangganController:
    """Controller untuk operasi Pelanggan."""

    def semua_pelanggan(self):
        session = get_session()
        try:
            return (
                session.query(Pelanggan)
                .options(selectinload(Pelanggan.pesanan_list))
                .order_by(Pelanggan.nama.asc())
                .all()
            )
        finally:
            session.close()

    def ambil_pelanggan(self, pelanggan_id):
        session = get_session()
        try:
            return (
                session.query(Pelanggan)
                .options(selectinload(Pelanggan.pesanan_list))
                .filter(Pelanggan.id == int(pelanggan_id))
                .first()
            )
        finally:
            session.close()

    def tambah_pelanggan(self, nama):
        """Menambahkan pelanggan baru dengan validasi data melalui setter model."""
        session = get_session()
        try:
            pel = Pelanggan()
            pel.set_nama(nama)  # Validasi nama pelanggan dieksekusi di setter

            session.add(pel)
            session.commit()
            return pel.id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def hapus_pelanggan(self, pelanggan_id):
        session = get_session()
        try:
            pel = session.query(Pelanggan).filter(Pelanggan.id == int(pelanggan_id)).first()
            if not pel:
                raise ValueError("Pelanggan tidak ditemukan.")
            session.delete(pel)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
