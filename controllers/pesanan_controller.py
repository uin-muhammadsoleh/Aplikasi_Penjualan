from datetime import datetime
from database.db import get_session
from models.detail_pesanan import DetailPesanan
from models.pesanan import Pesanan
from models.produk import Produk
from sqlalchemy.orm import joinedload, selectinload


class PesananController:
    """Controller untuk mengelola Pesanan dan DetailPesanan."""

    def semua_pesanan(self):
        session = get_session()
        try:
            return (
                session.query(Pesanan)
                .options(
                    joinedload(Pesanan.pelanggan),
                    selectinload(Pesanan.detail).joinedload(DetailPesanan.produk),
                )
                .order_by(Pesanan.id.desc())
                .all()
            )
        finally:
            session.close()

    def ambil_pesanan(self, pesanan_id):
        session = get_session()
        try:
            return (
                session.query(Pesanan)
                .options(
                    joinedload(Pesanan.pelanggan),
                    selectinload(Pesanan.detail).joinedload(DetailPesanan.produk),
                )
                .filter(Pesanan.id == int(pesanan_id))
                .first()
            )
        finally:
            session.close()

    def generate_nomor_pesanan(self):
        """Membuat nomor pesanan otomatis berbasis timestamp (contoh: ORD-20261110-XXXX)."""
        now = datetime.now()
        prefix = f"ORD-{now.strftime('%Y%m%d')}"
        session = get_session()
        try:
            count = session.query(Pesanan).count() + 1
            return f"{prefix}-{count:04d}"
        finally:
            session.close()

    def buat_pesanan(self, nomor: str, pelanggan_id: int | None, list_item: list[dict]):
        """Membuat pesanan baru menggunakan metode tambah_produk() dari class Pesanan.
        list_item: list of {'produk_id': int, 'jumlah': int}
        """
        nomor = (nomor or "").strip()
        if not nomor:
            raise ValueError("Nomor pesanan wajib diisi.")
        if not list_item:
            raise ValueError("Pesanan minimal harus memiliki 1 item produk.")

        session = get_session()
        try:
            pesanan = Pesanan()
            if hasattr(pesanan, "set_nomor"):
                pesanan.set_nomor(nomor)
            else:
                pesanan.nomor = nomor

            if hasattr(pesanan, "set_pelanggan_id"):
                pesanan.set_pelanggan_id(pelanggan_id)
            else:
                pesanan.pelanggan_id = pelanggan_id

            session.add(pesanan)

            for item in list_item:
                p_id = int(item["produk_id"])
                qty = int(item["jumlah"])
                if qty <= 0:
                    continue

                produk = session.query(Produk).filter(Produk.id == p_id).first()
                if not produk:
                    raise ValueError(f"Produk dengan ID {p_id} tidak ditemukan.")

                stok_tersedia = (
                    produk.get_stok() if hasattr(produk, "get_stok") else getattr(produk, "stok", 0)
                )
                nama_p = (
                    produk.get_nama() if hasattr(produk, "get_nama") else getattr(produk, "nama", "")
                )

                if stok_tersedia < qty:
                    raise ValueError(
                        f"Stok produk '{nama_p}' tidak mencukupi (sisa: {stok_tersedia}, diminta: {qty})."
                    )

                # Panggil method tambah_produk() sesuai Class Diagram
                pesanan.tambah_produk(produk=produk, jumlah=qty)

                # Kurangi stok produk
                sisa_stok = stok_tersedia - qty
                if hasattr(produk, "set_stok"):
                    produk.set_stok(sisa_stok)
                else:
                    produk.stok = sisa_stok

            session.commit()
            return pesanan.id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def hapus_pesanan(self, pesanan_id):
        session = get_session()
        try:
            pesanan = session.query(Pesanan).filter(Pesanan.id == int(pesanan_id)).first()
            if not pesanan:
                raise ValueError("Pesanan tidak ditemukan.")
            session.delete(pesanan)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
