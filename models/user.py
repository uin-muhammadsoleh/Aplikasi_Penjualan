import re
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from database.db import Base


class User(Base):
    """Model/tabel pengguna (user) pada database:
    - username: str
    - password_hash: str
    - nama_lengkap: str
    + get_username() / set_username()
    + get_password_hash() / set_password_hash()
    + get_nama_lengkap() / set_nama_lengkap()
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    _username = Column("username", String(50), unique=True, nullable=False, index=True)
    _password_hash = Column("password_hash", String(255), nullable=False)
    _nama_lengkap = Column("nama_lengkap", String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(
        self,
        username: str = "",
        password_hash: str = "",
        nama_lengkap: str = "",
        **kwargs,
    ):
        super().__init__(**kwargs)
        if username:
            self.set_username(username)
        else:
            self._username = ""
        if password_hash:
            self.set_password_hash(password_hash)
        else:
            self._password_hash = ""
        if nama_lengkap:
            self.set_nama_lengkap(nama_lengkap)
        else:
            self._nama_lengkap = ""

    # ==============================================================
    # GETTER & SETTER DENGAN VALIDASI: USERNAME
    # ==============================================================
    @hybrid_property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, val: str):
        self.set_username(val)

    def get_username(self) -> str:
        """Getter untuk username pengguna."""
        return self.username

    def set_username(self, val: str):
        """Setter untuk username dengan validasi format."""
        if val is None:
            raise ValueError("Username tidak boleh kosong.")
        val_str = str(val).strip().lower()
        if len(val_str) < 3 or len(val_str) > 30:
            raise ValueError("Username harus terdiri dari 3 hingga 30 karakter.")
        if not re.match(r"^[a-zA-Z0-9_]+$", val_str):
            raise ValueError("Username hanya boleh berisi huruf, angka, dan underscore (_).")
        self._username = val_str

    # ==============================================================
    # GETTER & SETTER DENGAN VALIDASI: NAMA LENGKAP
    # ==============================================================
    @hybrid_property
    def nama_lengkap(self) -> str:
        return self._nama_lengkap

    @nama_lengkap.setter
    def nama_lengkap(self, val: str):
        self.set_nama_lengkap(val)

    def get_nama_lengkap(self) -> str:
        """Getter untuk nama lengkap pengguna."""
        return self.nama_lengkap

    def set_nama_lengkap(self, val: str):
        """Setter untuk nama lengkap dengan validasi."""
        if val is None:
            raise ValueError("Nama lengkap tidak boleh kosong.")
        val_str = str(val).strip()
        if len(val_str) < 2:
            raise ValueError("Nama lengkap wajib diisi dan minimal 2 karakter.")
        if len(val_str) > 100:
            raise ValueError("Nama lengkap maksimal 100 karakter.")
        self._nama_lengkap = val_str

    # ==============================================================
    # GETTER & SETTER DENGAN VALIDASI: PASSWORD HASH
    # ==============================================================
    @hybrid_property
    def password_hash(self) -> str:
        return self._password_hash

    @password_hash.setter
    def password_hash(self, val: str):
        self.set_password_hash(val)

    def get_password_hash(self) -> str:
        """Getter untuk hash password."""
        return self.password_hash

    def set_password_hash(self, val: str):
        """Setter untuk hash password."""
        if not val or not str(val).strip():
            raise ValueError("Password hash tidak boleh kosong.")
        self._password_hash = str(val).strip()

    def __repr__(self):
        return f"User(id={self.id}, username={self.username!r})"
