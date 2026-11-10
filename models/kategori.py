from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base


class Kategori(Base):
    """Model Kategori sesuai Class Diagram:
    - nama
    - daftar_produk
    + tambah_produk()
    """

    __tablename__ = "kategori"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100), nullable=False, unique=True)

    # Relasi Aggregation ke Produk (daftar_produk) dengan lazy="selectin"
    daftar_produk = relationship(
        "Produk",
        back_populates="kategori",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __init__(self, nama: str = "", **kwargs):
        super().__init__(nama=nama, **kwargs)

    def tambah_produk(self, produk):
        """Menambahkan objek produk ke dalam daftar_produk (+ tambah_produk())."""
        if produk not in self.daftar_produk:
            self.daftar_produk.append(produk)
            produk.kategori = self

    def __repr__(self):
        return f"Kategori(id={self.id}, nama={self.nama!r})"
