from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from database.db import Base


class Kategori(Base):
    """Model Kategori sesuai Class Diagram:
    - nama: str
    - daftar_produk: list
    + get_nama() / set_nama()
    + get_daftar_produk()
    + tambah_produk()
    """

    __tablename__ = "kategori"

    id = Column(Integer, primary_key=True, autoincrement=True)
    _nama = Column("nama", String(100), nullable=False, unique=True)

    # Relasi Aggregation ke Produk (daftar_produk) dengan lazy="selectin"
    daftar_produk = relationship(
        "Produk",
        back_populates="kategori",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __init__(self, nama: str = "", **kwargs):
        super().__init__(**kwargs)
        if nama:
            self.set_nama(nama)
        else:
            self._nama = ""

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
        """Getter untuk nama kategori."""
        return self.nama

    def set_nama(self, val: str):
        """Setter untuk nama kategori dengan validasi ketat."""
        if val is None:
            raise ValueError("Nama kategori tidak boleh kosong.")
        val_str = str(val).strip()
        if len(val_str) < 2:
            raise ValueError("Nama kategori wajib diisi dan minimal 2 karakter.")
        if len(val_str) > 100:
            raise ValueError("Nama kategori maksimal 100 karakter.")
        self._nama = val_str

    # ==============================================================
    # GETTER & SETTER: DAFTAR PRODUK
    # ==============================================================
    def get_daftar_produk(self):
        """Getter untuk koleksi daftar_produk."""
        return self.daftar_produk

    def set_daftar_produk(self, daftar: list):
        """Setter untuk koleksi daftar_produk."""
        self.daftar_produk = daftar

    # ==============================================================
    # METHOD BISNIS SESUAI CLASS DIAGRAM
    # ==============================================================
    def tambah_produk(self, produk):
        """Menambahkan objek produk ke dalam daftar_produk (+ tambah_produk())."""
        if produk not in self.daftar_produk:
            self.daftar_produk.append(produk)
            produk.kategori = self

    def __repr__(self):
        return f"Kategori(id={self.id}, nama={self.nama!r})"
