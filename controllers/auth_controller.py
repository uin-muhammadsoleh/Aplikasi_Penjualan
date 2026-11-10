import hashlib
import os
import re
import streamlit as st
from database.db import get_session
from models.user import User


def hash_password(password: str) -> str:
    """Mengenkripsi password menggunakan PBKDF2-HMAC-SHA256 dengan salt acak."""
    salt = os.urandom(16).hex()
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    ).hex()
    return f"{salt}${pwd_hash}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Mencocokkan password dengan hash yang tersimpan."""
    if not stored_hash or "$" not in stored_hash:
        return False
    salt, pwd_hash = stored_hash.split("$", 1)
    calculated_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    ).hex()
    return calculated_hash == pwd_hash


class AuthController:
    """Controller untuk menangani pendaftaran, autentikasi, dan status sesi pengguna."""

    def daftar_user(
        self, username: str, password: str, konfirmasi_password: str, nama_lengkap: str
    ) -> tuple[bool, str]:
        username = (username or "").strip().lower()
        nama_lengkap = (nama_lengkap or "").strip()
        password = password or ""
        konfirmasi_password = konfirmasi_password or ""

        if not username or not nama_lengkap or not password:
            return False, "Semua bidang formulir wajib diisi."

        if len(username) < 3 or len(username) > 30:
            return False, "Username harus terdiri dari 3 hingga 30 karakter."

        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return False, "Username hanya boleh berisi huruf, angka, dan underscore (_)."

        if len(password) < 6:
            return False, "Password minimal 6 karakter."

        if password != konfirmasi_password:
            return False, "Konfirmasi password tidak cocok."

        session = get_session()
        try:
            existing = session.query(User).filter(User.username == username).first()
            if existing:
                return False, f"Username '{username}' sudah terdaftar. Gunakan username lain."

            new_user = User(
                username=username,
                password_hash=hash_password(password),
                nama_lengkap=nama_lengkap,
            )
            session.add(new_user)
            session.commit()
            return True, "Pendaftaran berhasil! Silakan masuk dengan akun Anda."
        except Exception as e:
            session.rollback()
            return False, f"Terjadi kesalahan saat pendaftaran: {str(e)}"
        finally:
            session.close()

    def login_user(self, username: str, password: str) -> tuple[bool, str, User | None]:
        username = (username or "").strip().lower()
        password = password or ""

        if not username or not password:
            return False, "Username dan password wajib diisi.", None

        session = get_session()
        try:
            user = session.query(User).filter(User.username == username).first()
            if not user or not verify_password(password, user.password_hash):
                return False, "Username atau password salah.", None
            return True, "Login berhasil!", user
        finally:
            session.close()

    @staticmethod
    def is_logged_in() -> bool:
        """Memeriksa apakah ada pengguna yang aktif login dalam session state."""
        return st.session_state.get("authenticated", False)

    @staticmethod
    def get_current_user() -> dict | None:
        """Mengambil data pengguna yang sedang login saat ini."""
        return st.session_state.get("user")

    @staticmethod
    def login_session(user: User):
        """Menyimpan data login ke dalam Streamlit session state."""
        st.session_state["authenticated"] = True
        st.session_state["user"] = {
            "id": user.id,
            "username": user.username,
            "nama_lengkap": user.nama_lengkap,
        }

    @staticmethod
    def logout():
        """Menghapus sesi login dan mereset session state."""
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.rerun()

    def render_sidebar_user_info(self):
        """Menampilkan panel info pengguna dan tombol logout pada sidebar."""
        user = self.get_current_user()
        if user:
            with st.sidebar:
                st.markdown("---")
                st.markdown("### 👤 Profil Pengguna")
                st.markdown(f"**{user['nama_lengkap']}**")
                st.caption(f"Username: `@{user['username']}`")
                if st.button("🚪 Keluar (Logout)", use_container_width=True, type="secondary"):
                    self.logout()


def seed_default_user():
    """Membuat pengguna bawaan (admin / admin123) jika belum ada user di database."""
    session = get_session()
    try:
        if session.query(User).count() == 0:
            admin_user = User(
                username="admin",
                password_hash=hash_password("admin123"),
                nama_lengkap="Administrator",
            )
            session.add(admin_user)
            session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()
