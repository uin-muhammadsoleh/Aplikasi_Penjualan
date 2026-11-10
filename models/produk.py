from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from database.db import Base


class Produk(Base):
    """Model Produk sesuai Class Diagram:
    - nama: str
    - harga: float
    - stok: int
    - kategori_id: int | None
    + get_nama() / set_nama()
    + get_harga() / set_harga()
    + get_stok() / set_stok()
    + get_kategori_id() / set_kategori_id()
    + get_info(): str
    """

    __tablename__ = "produk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    _nama = Column("nama", String(150), nullable=False)
    _harga = Column("harga", Float, nullable=False, default=0.0)
    _stok = Column("stok", Integer, nullable=False, default=0)

    # Relasi Aggregation dengan Kategori
    _kategori_id = Column(
        "kategori_id", Integer, ForeignKey("kategori.id", ondelete="SET NULL"), nullable=True
    )
    kategori = relationship(
        "Kategori",
        back_populates="daftar_produk",
        foreign_keys=[_kategori_id],
        lazy="joined",
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
        super().__init__(**kwargs)
        if kategori is not None:
            self.set_kategori(kategori)
        if kategori_id is not None:
            self.set_kategori_id(kategori_id)
        if nama:
            self.set_nama(nama)
        else:
            self._nama = ""
        self.set_harga(harga)
        self.set_stok(stok)

    # ==============================================================
    # GETTER & SETTER DENGAN VALIDASI: NAMA
    # ==============================================================
    @hybrid_property
    def nama(self) -> str:
        return self._nama

    @nama.setter
    def nama(self, val: str):
        self.set_nama(val)

    def get_nama(self) -> str:
        """Getter untuk nama produk."""
        return self.nama

    def set_nama(self, val: str):
        """Setter untuk nama produk dengan validasi ketat."""
        if val is None:
            raise ValueError("Nama produk tidak boleh kosong.")
        val_str = str(val).strip()
        if len(val_str) < 2:
            raise ValueError("Nama produk wajib diisi dan minimal 2 karakter.")
        if len(val_str) > 150:
            raise ValueError("Nama produk maksimal 150 karakter.")
        self._nama = val_str

    # ==============================================================
    # GETTER & SETTER DENGAN VALIDASI: HARGA
    # ==============================================================
    @hybrid_property
    def harga(self) -> float:
        return self._harga

    @harga.setter
    def harga(self, val: float):
        self.set_harga(val)

    def get_harga(self) -> float:
        """Getter untuk harga produk."""
        return float(self.harga) if self.harga is not None else 0.0

    def set_harga(self, val: float):
        """Setter untuk harga produk dengan validasi angka non-negatif."""
        try:
            val_float = float(val)
        except (ValueError, TypeError):
            raise ValueError("Harga produk harus berupa angka yang valid.")
        if val_float < 0:
            raise ValueError("Harga produk tidak boleh bernilai negatif (minimal Rp 0).")
        self._harga = val_float

    # ==============================================================
    # GETTER & SETTER DENGAN VALIDASI: STOK
    # ==============================================================
    @hybrid_property
    def stok(self) -> int:
        return self._stok

    @stok.setter
    def stok(self, val: int):
        self.set_stok(val)

    def get_stok(self) -> int:
        """Getter untuk stok produk."""
        return int(self.stok) if self.stok is not None else 0

    def set_stok(self, val: int):
        """Setter untuk stok produk dengan validasi bilangan bulat non-negatif."""
        try:
            val_int = int(val)
        except (ValueError, TypeError):
            raise ValueError("Stok produk harus berupa bilangan bulat.")
        if val_int < 0:
            raise ValueError("Stok produk tidak boleh bernilai negatif (minimal 0).")
        self._stok = val_int

    # ==============================================================
    # GETTER & SETTER: KATEGORI_ID & KATEGORI
    # ==============================================================
    @hybrid_property
    def kategori_id(self) -> int | None:
        return self._kategori_id

    @kategori_id.setter
    def kategori_id(self, val: int | None):
        self.set_kategori_id(val)

    def get_kategori_id(self) -> int | None:
        """Getter untuk foreign key kategori_id."""
        return self.kategori_id

    def set_kategori_id(self, val: int | None):
        """Setter untuk kategori_id."""
        if val is None or val == "" or val == 0:
            self._kategori_id = None
        else:
            try:
                self._kategori_id = int(val)
            except (ValueError, TypeError):
                raise ValueError("Kategori ID harus berupa bilangan bulat.")

    def get_kategori(self):
        """Getter untuk objek relasi Kategori."""
        return self.kategori

    def set_kategori(self, kategori_obj):
        """Setter untuk objek relasi Kategori."""
        self.kategori = kategori_obj
        if kategori_obj and hasattr(kategori_obj, "id") and kategori_obj.id:
            self._kategori_id = kategori_obj.id

    # ==============================================================
    # METHOD BISNIS
    # ==============================================================
    def get_info(self) -> str:
        """Mengembalikan informasi ringkas tentang produk (+ get_info())."""
        kategori_nama = self.kategori.nama if self.kategori else "Tanpa Kategori"
        return f"{self.nama} | Kategori: {kategori_nama} | Harga: Rp {self.harga:,.2f} | Stok: {self.stok}"

    def __repr__(self):
        return f"Produk(id={self.id}, nama={self.nama!r}, harga={self.harga}, stok={self.stok})"
