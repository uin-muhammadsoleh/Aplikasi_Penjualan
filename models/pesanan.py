from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base


class Pesanan(Base):
    """Model Pesanan sesuai Class Diagram:
    - nomor
    - detail (Composition dengan DetailPesanan)
    + tambah_produk()
    """

    __tablename__ = "pesanan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nomor = Column(String(50), unique=True, nullable=False, index=True)
    tanggal = Column(DateTime, default=datetime.utcnow)

    pelanggan_id = Column(Integer, ForeignKey("pelanggan.id"), nullable=True)
    pelanggan = relationship(
        "Pelanggan", back_populates="pesanan_list", lazy="joined"
    )

    # detail (Composition: cascade all, delete-orphan) dengan lazy="selectin"
    detail = relationship(
        "DetailPesanan",
        back_populates="pesanan",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __init__(self, nomor: str = "", pelanggan_id: int | None = None, **kwargs):
        super().__init__(nomor=nomor, pelanggan_id=pelanggan_id, **kwargs)

    def tambah_produk(self, produk, jumlah: int = 1):
        """Menambahkan produk ke dalam pesanan (+ tambah_produk())."""
        from models.detail_pesanan import DetailPesanan

        detail_item = DetailPesanan(produk=produk, jumlah=jumlah)
        self.detail.append(detail_item)
        return detail_item

    def get_total_pesanan(self) -> float:
        """Menghitung total keseluruhan nilai pesanan dari semua detail."""
        return sum(d.get_total() for d in self.detail)

    def __repr__(self):
        return f"Pesanan(id={self.id}, nomor={self.nomor!r})"
