from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base


class Produk(Base):
    """Model Produk sesuai Class Diagram:
    - nama
    - harga
    + get_info()
    """

    __tablename__ = "produk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(150), nullable=False)
    harga = Column(Float, nullable=False, default=0.0)
    stok = Column(Integer, nullable=False, default=0)

    # Relasi Aggregation dengan Kategori (lazy="joined" untuk eager loading)
    kategori_id = Column(
        Integer, ForeignKey("kategori.id", ondelete="SET NULL"), nullable=True
    )
    kategori = relationship(
        "Kategori", back_populates="daftar_produk", lazy="joined"
    )

    def __init__(
        self,
        nama: str = "",
        harga: float = 0.0,
        stok: int = 0,
        kategori_id: int | None = None,
        kategori=None,
        **kwargs,
    ):
        if kategori is not None:
            kwargs["kategori"] = kategori
        if kategori_id is not None:
            kwargs["kategori_id"] = kategori_id
        super().__init__(
            nama=nama,
            harga=harga,
            stok=stok,
            **kwargs,
        )

    def get_info(self) -> str:
        """Mengembalikan informasi ringkas tentang produk (+ get_info())."""
        kategori_nama = self.kategori.nama if self.kategori else "Tanpa Kategori"
        return f"{self.nama} | Kategori: {kategori_nama} | Harga: Rp {self.harga:,.2f} | Stok: {self.stok}"

    def __repr__(self):
        return f"Produk(id={self.id}, nama={self.nama!r}, harga={self.harga})"
