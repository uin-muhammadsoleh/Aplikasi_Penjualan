import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Membaca konfigurasi dari file .env jika tersedia.
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# Default menggunakan SQLite. Untuk MySQL, isi DATABASE_URL di file .env.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{(ROOT_DIR / 'database' / 'manajemen_produk.db').as_posix()}",
)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

# expire_on_commit=False mencegah pelepasan atribut objek setelah commit/tutup session
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)
Base = declarative_base()


def init_db():
    """Membuat tabel berdasarkan model yang terdaftar dan inisialisasi data bawaan."""
    from models.detail_pesanan import DetailPesanan  # noqa: F401
    from models.kategori import Kategori  # noqa: F401
    from models.pelanggan import Pelanggan  # noqa: F401
    from models.pesanan import Pesanan  # noqa: F401
    from models.produk import Produk  # noqa: F401
    from models.user import User  # noqa: F401

    Base.metadata.create_all(bind=engine)

    from controllers.auth_controller import seed_default_user

    seed_default_user()
    seed_default_data()


def seed_default_data():
    """Membuat data awal Kategori dan Pelanggan jika belum ada."""
    session = get_session()
    try:
        from models.kategori import Kategori
        from models.pelanggan import Pelanggan

        if session.query(Kategori).count() == 0:
            kat1 = Kategori(nama="Elektronik")
            kat2 = Kategori(nama="Makanan & Minuman")
            kat3 = Kategori(nama="Pakaian & Aksesoris")
            session.add_all([kat1, kat2, kat3])
            session.commit()

        if session.query(Pelanggan).count() == 0:
            pel1 = Pelanggan(nama="Budi Santoso")
            pel2 = Pelanggan(nama="Siti Rahma")
            pel3 = Pelanggan(nama="Ahmad Fauzi")
            session.add_all([pel1, pel2, pel3])
            session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


def get_session():
    """Membuat session database."""
    return SessionLocal()


def get_database_info():
    """Mengembalikan jenis database aktif tanpa membocorkan kredensial."""
    if DATABASE_URL.startswith("sqlite"):
        return "SQLite"
    if DATABASE_URL.startswith("mysql"):
        return "MySQL"
    return "Database dari konfigurasi DATABASE_URL"
