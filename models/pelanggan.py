from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base


class Pelanggan(Base):
    """Model Pelanggan sesuai Class Diagram:
    - nama
    + lihat_produk()
    """

    __tablename__ = "pelanggan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100), nullable=False)

    pesanan_list = relationship(
        "Pesanan", back_populates="pelanggan", lazy="selectin"
    )

    def __init__(self, nama: str = "", **kwargs):
        super().__init__(nama=nama, **kwargs)

    def lihat_produk(self, daftar_produk=None):
        """Menampilkan atau mengambil daftar produk (+ lihat_produk())."""
        if daftar_produk is not None:
            return daftar_produk
        from database.db import get_session
        from models.produk import Produk
        from sqlalchemy.orm import joinedload

        session = get_session()
        try:
            return session.query(Produk).options(joinedload(Produk.kategori)).all()
        finally:
            session.close()

    def __repr__(self):
        return f"Pelanggan(id={self.id}, nama={self.nama!r})"
