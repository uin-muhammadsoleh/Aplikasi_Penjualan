from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database.db import Base


class DetailPesanan(Base):
    """Model DetailPesanan sesuai Class Diagram:
    - produk
    - jumlah
    + get_total()
    """

    __tablename__ = "detail_pesanan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pesanan_id = Column(
        Integer, ForeignKey("pesanan.id", ondelete="CASCADE"), nullable=False
    )
    produk_id = Column(Integer, ForeignKey("produk.id"), nullable=False)
    jumlah = Column(Integer, nullable=False, default=1)

    pesanan = relationship("Pesanan", back_populates="detail", lazy="joined")
    produk = relationship("Produk", lazy="joined")

    def __init__(
        self, produk=None, jumlah: int = 1, pesanan_id: int | None = None, **kwargs
    ):
        if produk is not None:
            kwargs["produk"] = produk
            if hasattr(produk, "id") and produk.id:
                kwargs["produk_id"] = produk.id
        if pesanan_id is not None:
            kwargs["pesanan_id"] = pesanan_id
        super().__init__(jumlah=jumlah, **kwargs)

    def get_total(self) -> float:
        """Menghitung subtotal untuk item ini: produk.harga * jumlah (+ get_total())."""
        if self.produk:
            return float(self.produk.harga) * int(self.jumlah)
        return 0.0

    def __repr__(self):
        return f"DetailPesanan(id={self.id}, produk_id={self.produk_id}, jumlah={self.jumlah})"
