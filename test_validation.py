import unittest
from models.produk import Produk
from models.kategori import Kategori
from models.pelanggan import Pelanggan
from models.pesanan import Pesanan
from models.detail_pesanan import DetailPesanan
from models.user import User


class TestModelValidation(unittest.TestCase):
    def test_produk_valid(self):
        p = Produk()
        p.set_nama("Mouse Logitech G102")
        p.set_harga(250000.0)
        p.set_stok(20)
        p.set_kategori_id(1)

        self.assertEqual(p.get_nama(), "Mouse Logitech G102")
        self.assertEqual(p.get_harga(), 250000.0)
        self.assertEqual(p.get_stok(), 20)
        self.assertEqual(p.get_kategori_id(), 1)

    def test_produk_invalid_nama(self):
        p = Produk()
        # Empty
        with self.assertRaises(ValueError):
            p.set_nama("")
        # Too short
        with self.assertRaises(ValueError):
            p.set_nama("A")
        # None
        with self.assertRaises(ValueError):
            p.set_nama(None)
        # Exceeds max length
        with self.assertRaises(ValueError):
            p.set_nama("x" * 151)

    def test_produk_invalid_harga(self):
        p = Produk()
        # Negative
        with self.assertRaises(ValueError):
            p.set_harga(-1000)
        # Not a number
        with self.assertRaises(ValueError):
            p.set_harga("invalid_price")

    def test_produk_invalid_stok(self):
        p = Produk()
        # Negative
        with self.assertRaises(ValueError):
            p.set_stok(-5)
        # Not an integer
        with self.assertRaises(ValueError):
            p.set_stok("invalid_stock")

    def test_kategori_valid_and_invalid(self):
        k = Kategori()
        k.set_nama("Elektronik")
        self.assertEqual(k.get_nama(), "Elektronik")

        # Empty
        with self.assertRaises(ValueError):
            k.set_nama("")
        # Short
        with self.assertRaises(ValueError):
            k.set_nama("E")
        # None
        with self.assertRaises(ValueError):
            k.set_nama(None)

    def test_pelanggan_valid_and_invalid(self):
        pel = Pelanggan()
        pel.set_nama("Budi Pratama")
        self.assertEqual(pel.get_nama(), "Budi Pratama")

        # Empty
        with self.assertRaises(ValueError):
            pel.set_nama("")
        # Short
        with self.assertRaises(ValueError):
            pel.set_nama("B")

    def test_pesanan_valid_and_invalid(self):
        pes = Pesanan()
        pes.set_nomor("ORD-2026-0001")
        self.assertEqual(pes.get_nomor(), "ORD-2026-0001")

        # Empty
        with self.assertRaises(ValueError):
            pes.set_nomor("")
        # Short
        with self.assertRaises(ValueError):
            pes.set_nomor("NO")

    def test_detail_pesanan_valid_and_invalid(self):
        p = Produk()
        p.set_nama("Keyboard Mec")
        p.set_harga(500000)
        p.set_stok(10)

        dp = DetailPesanan(produk=p, jumlah=3)
        self.assertEqual(dp.get_jumlah(), 3)
        self.assertEqual(dp.get_total(), 1500000.0)

        # Jumlah <= 0
        with self.assertRaises(ValueError):
            dp.set_jumlah(0)
        with self.assertRaises(ValueError):
            dp.set_jumlah(-2)

    def test_user_valid_and_invalid(self):
        u = User()
        u.set_username("budi_santoso")
        u.set_nama_lengkap("Budi Santoso")
        u.set_password_hash("some_hash")

        self.assertEqual(u.get_username(), "budi_santoso")
        self.assertEqual(u.get_nama_lengkap(), "Budi Santoso")

        # Invalid username (special characters not allowed)
        with self.assertRaises(ValueError):
            u.set_username("budi@santoso!")
        # Short username
        with self.assertRaises(ValueError):
            u.set_username("ab")
        # Empty nama lengkap
        with self.assertRaises(ValueError):
            u.set_nama_lengkap("")


if __name__ == "__main__":
    unittest.main()
