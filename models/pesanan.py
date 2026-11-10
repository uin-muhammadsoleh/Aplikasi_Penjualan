from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from database.db import Base


class Pesanan(Base):
    """Model Pesanan sesuai Class Diagram:
    - nomor: str
    - detail: list (Composition dengan DetailPesanan)
    + get_nomor() / set_nomor()
    + get_pelanggan_id() / set_pelanggan_id()
    + get_detail() / set_detail()
    + tambah_produk(produk, jumlah)
    + get_total_pesanan()
    """

    __tablename__ = "pesanan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    _nomor = Column("nomor", String(50), unique=True, nullable=False, index=True)
    tanggal = Column(DateTime, default=datetime.utcnow)

    _pelanggan_id = Column("pelanggan_id", Integer, ForeignKey("pelanggan.id"), nullable=True)
    pelanggan = relationship(
        "Pelanggan", back_populates="pesanan_list", foreign_keys=[_pelanggan_id], lazy="joined"
    )

    # detail (Composition: cascade all, delete-orphan) dengan lazy="selectin"
    detail = relationship(
        "DetailPesanan",
        back_populates="pesanan",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __init__(self, nomor: str = "", pelanggan_id: int | None = None, **kwargs):
        super().__init__(**kwargs)
        if nomor:
            self.set_nomor(nomor)
        else:
            self._nomor = ""
        self.set_pelanggan_id(pelanggan_id)

    # ==============================================================
    # GETTER & SETTER DENGAN VALIDASI: NOMOR
    # ==============================================================
    @hybrid_property
    def nomor(self) -> str:
        return self._nomor

    @nomor.setter
    def nomor(self, val: str):
        self.set_nomor(val)

    def get_nomor(self) -> str:
        """Getter untuk nomor pesanan."""
        return self.nomor

    def set_nomor(self, val: str):
        """Setter untuk nomor pesanan dengan validasi."""
        if val is None:
            raise ValueError("Nomor pesanan tidak boleh kosong.")
        val_str = str(val).strip()
        if len(val_str) < 3:
            raise ValueError("Nomor pesanan wajib diisi dan minimal 3 karakter.")
        if len(val_str) > 50:
            raise ValueError("Nomor pesanan maksimal 50 karakter.")
        self._nomor = val_str

    # ==============================================================
    # GETTER & SETTER: PELANGGAN_ID & PELANGGAN
    # ==============================================================
    @hybrid_property
    def pelanggan_id(self) -> int | None:
        return self._pelanggan_id

    @pelanggan_id.setter
    def pelanggan_id(self, val: int | None):
        self.set_pelanggan_id(val)

    def get_pelanggan_id(self) -> int | None:
        """Getter untuk foreign key pelanggan_id."""
        return self.pelanggan_id

    def set_pelanggan_id(self, val: int | None):
        """Setter untuk foreign key pelanggan_id."""
        if val is None or val == "" or val == 0:
            self._pelanggan_id = None
        else:
            try:
                self._pelanggan_id = int(val)
            except (ValueError, TypeError):
                raise ValueError("Pelanggan ID harus berupa bilangan bulat.")

    def get_pelanggan(self):
        """Getter untuk objek relasi Pelanggan."""
        return self.pelanggan

    def set_pelanggan(self, pelanggan_obj):
        """Setter untuk objek relasi Pelanggan."""
        self.pelanggan = pelanggan_obj
        if pelanggan_obj and hasattr(pelanggan_obj, "id") and pelanggan_obj.id:
            self._pelanggan_id = pelanggan_obj.id

    # ==============================================================
    # GETTER & SETTER: DETAIL PESANAN
    # ==============================================================
    def get_detail(self):
        """Getter untuk daftar DetailPesanan."""
        return self.detail

    def set_detail(self, detail_list: list):
        """Setter untuk daftar DetailPesanan."""
        self.detail = detail_list

    def get_tanggal(self) -> datetime:
        """Getter untuk tanggal pesanan dibuat."""
        return self.tanggal

    def set_tanggal(self, tgl: datetime):
        """Setter untuk tanggal pesanan dibuat."""
        self.tanggal = tgl

    # ==============================================================
    # METHOD BISNIS SESUAI CLASS DIAGRAM
    # ==============================================================
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
