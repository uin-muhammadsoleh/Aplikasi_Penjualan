from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from database.db import Base


class DetailPesanan(Base):
    """Model DetailPesanan sesuai Class Diagram:
    - produk: Produk
    - jumlah: int
    + get_produk() / set_produk()
    + get_jumlah() / set_jumlah()
    + get_total(): float
    """

    __tablename__ = "detail_pesanan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pesanan_id = Column(
        Integer, ForeignKey("pesanan.id", ondelete="CASCADE"), nullable=False
    )
    _produk_id = Column("produk_id", Integer, ForeignKey("produk.id"), nullable=False)
    _jumlah = Column("jumlah", Integer, nullable=False, default=1)

    pesanan = relationship("Pesanan", back_populates="detail", lazy="joined")
    produk = relationship("Produk", foreign_keys=[_produk_id], lazy="joined")

    def __init__(
        self, produk=None, jumlah: int = 1, pesanan_id: int | None = None, **kwargs
    ):
        super().__init__(**kwargs)
        if produk is not None:
            self.set_produk(produk)
        if pesanan_id is not None:
            self.pesanan_id = pesanan_id
        self.set_jumlah(jumlah)

    # ==============================================================
    # GETTER & SETTER DENGAN VALIDASI: JUMLAH
    # ==============================================================
    @hybrid_property
    def jumlah(self) -> int:
        return self._jumlah

    @jumlah.setter
    def jumlah(self, val: int):
        self.set_jumlah(val)

    def get_jumlah(self) -> int:
        """Getter untuk jumlah pembelian."""
        return int(self.jumlah) if self.jumlah is not None else 1

    def set_jumlah(self, val: int):
        """Setter untuk jumlah pembelian dengan validasi positif (minimal 1)."""
        try:
            val_int = int(val)
        except (ValueError, TypeError):
            raise ValueError("Jumlah pesanan harus berupa bilangan bulat.")
        if val_int < 1:
            raise ValueError("Jumlah pesanan minimal 1 item.")
        self._jumlah = val_int

    # ==============================================================
    # GETTER & SETTER: PRODUK_ID & PRODUK
    # ==============================================================
    @hybrid_property
    def produk_id(self) -> int:
        return self._produk_id

    @produk_id.setter
    def produk_id(self, val: int):
        self.set_produk_id(val)

    def get_produk_id(self) -> int:
        """Getter untuk foreign key produk_id."""
        return self.produk_id

    def set_produk_id(self, val: int):
        """Setter untuk foreign key produk_id."""
        try:
            val_int = int(val)
        except (ValueError, TypeError):
            raise ValueError("Produk ID harus berupa bilangan bulat.")
        if val_int <= 0:
            raise ValueError("Produk ID tidak valid.")
        self._produk_id = val_int

    def get_produk(self):
        """Getter untuk objek relasi Produk."""
        return self.produk

    def set_produk(self, produk_obj):
        """Setter untuk objek relasi Produk."""
        self.produk = produk_obj
        if produk_obj and hasattr(produk_obj, "id") and produk_obj.id:
            self._produk_id = produk_obj.id

    # ==============================================================
    # METHOD BISNIS SESUAI CLASS DIAGRAM
    # ==============================================================
    def get_total(self) -> float:
        """Menghitung subtotal untuk item ini: produk.harga * jumlah (+ get_total())."""
        if self.produk:
            return float(self.produk.get_harga()) * int(self.get_jumlah())
        return 0.0

    def __repr__(self):
        return f"DetailPesanan(id={self.id}, produk_id={self.produk_id}, jumlah={self.jumlah})"
