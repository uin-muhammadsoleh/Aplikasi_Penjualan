from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from database.db import Base


class Pelanggan(Base):
    """Model Pelanggan sesuai Class Diagram:
    - nama: str
    + get_nama() / set_nama()
    + lihat_produk(): list
    """

    __tablename__ = "pelanggan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    _nama = Column("nama", String(100), nullable=False)

    pesanan_list = relationship(
        "Pesanan", back_populates="pelanggan", lazy="selectin"
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
        """Getter untuk nama pelanggan."""
        return self.nama

    def set_nama(self, val: str):
        """Setter untuk nama pelanggan dengan validasi ketat."""
        if val is None:
            raise ValueError("Nama pelanggan tidak boleh kosong.")
        val_str = str(val).strip()
        if len(val_str) < 2:
            raise ValueError("Nama pelanggan wajib diisi dan minimal 2 karakter.")
        if len(val_str) > 100:
            raise ValueError("Nama pelanggan maksimal 100 karakter.")
        self._nama = val_str

    # ==============================================================
    # GETTER & SETTER: PESANAN LIST
    # ==============================================================
    def get_pesanan_list(self):
        """Getter untuk relasi riwayat pesanan pelanggan."""
        return self.pesanan_list

    def set_pesanan_list(self, pesanan_list):
        """Setter untuk relasi riwayat pesanan pelanggan."""
        self.pesanan_list = pesanan_list

    # ==============================================================
    # METHOD BISNIS SESUAI CLASS DIAGRAM
    # ==============================================================
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
