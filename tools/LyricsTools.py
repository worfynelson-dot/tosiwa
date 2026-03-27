"""
lyrics_skill.py — All-in-one Lyrics Search Skill untuk OpenClaw
Tidak perlu install library eksternal selain requests.
Install: pip install requests
"""

import requests

# ==============================
# BASE CONFIG
# ==============================

BASE_URL = "https://api.lexcode.biz.id/api/tools/lyrics"
TIMEOUT = 10


# ==============================
# SKILL MANIFEST (pengganti skill.json)
# ==============================

SKILL_MANIFEST = {
    "name": "lyrics_search",
    "version": "1.0.0",
    "description": "Cari lirik lagu berdasarkan judul. Bisa ambil lirik plain, lirik synced (dengan timestamp), info lagu, dan pilih hasil ke berapa.",
    "author": "Adit",
    "functions": [
        {
            "name": "search_lyrics",
            "description": "Cari lirik lagu berdasarkan judul. Mengembalikan daftar hasil lagu yang cocok.",
            "parameters": {
                "title": {"type": "string", "description": "Judul lagu yang dicari, contoh: 'Obsessed' atau 'Espresso Sabrina'"}
            }
        },
        {
            "name": "get_lyrics",
            "description": "Ambil lirik lengkap dari sebuah lagu. Bisa pilih hasil ke-berapa kalau ada banyak.",
            "parameters": {
                "title": {"type": "string", "description": "Judul lagu yang dicari"},
                "index": {"type": "integer", "description": "Nomor hasil yang dipilih (mulai dari 1, default: 1)", "default": 1},
                "mode": {"type": "string", "description": "'plain' untuk lirik biasa, 'synced' untuk lirik dengan timestamp. Default: 'plain'", "default": "plain"}
            }
        },
        {
            "name": "get_song_info",
            "description": "Ambil info lagu (judul, artis, album, durasi) tanpa lirik.",
            "parameters": {
                "title": {"type": "string", "description": "Judul lagu yang dicari"},
                "index": {"type": "integer", "description": "Nomor hasil yang dipilih (default: 1)", "default": 1}
            }
        }
    ]
}


# ==============================
# HELPER
# ==============================

def _fetch(title: str) -> dict:
    """Fetch raw data dari API."""
    try:
        response = requests.get(BASE_URL, params={"title": title}, timeout=TIMEOUT)
        data = response.json()

        if not data.get("success"):
            return {"success": False, "message": "❌ Lagu tidak ditemukan."}
        if not data.get("results"):
            return {"success": False, "message": "❌ Tidak ada hasil untuk pencarian ini."}

        return {"success": True, "data": data}

    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "❌ Tidak ada koneksi internet."}
    except requests.exceptions.Timeout:
        return {"success": False, "message": "❌ Request timeout. Coba lagi."}
    except Exception as e:
        return {"success": False, "message": f"❌ Error: {str(e)}"}


def _format_duration(seconds: int) -> str:
    """Format durasi dari detik ke mm:ss."""
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"


def _get_result(data: dict, index: int):
    """Ambil satu hasil berdasarkan index (1-based)."""
    results = data.get("results", [])
    if index < 1 or index > len(results):
        return None
    return results[index - 1]


# ==============================
# FUNGSI 1 — SEARCH LYRICS (daftar hasil)
# ==============================

def search_lyrics(title: str) -> dict:
    """
    Cari lagu berdasarkan judul, tampilkan daftar hasilnya.
    Contoh: search_lyrics("Espresso")
    """
    fetch = _fetch(title)
    if not fetch["success"]:
        return fetch

    data = fetch["data"]
    results = data["results"]
    total = data["total"]

    lines = [f"🎵 **Hasil pencarian: \"{title}\"** ({total} lagu ditemukan)\n━━━━━━━━━━━━━━━━━━"]

    for item in results:
        duration = _format_duration(item.get("duration", 0))
        instrumental = "🎹 Instrumental" if item.get("instrumental") else "🎤 Ada lirik"
        lines.append(
            f"\n**{item['no']}. {item['title']}**"
            f"\n   👤 Artis: {item['artist']}"
            f"\n   💿 Album: {item['album']}"
            f"\n   ⏱️ Durasi: {duration}"
            f"\n   {instrumental}"
        )

    lines.append("\n━━━━━━━━━━━━━━━━━━")
    lines.append("💬 Ketik nomor lagu untuk lihat liriknya!")

    return {
        "success": True,
        "total": total,
        "results": results,
        "message": "\n".join(lines)
    }


# ==============================
# FUNGSI 2 — GET LYRICS (lirik lengkap)
# ==============================

def get_lyrics(title: str, index: int = 1, mode: str = "plain") -> dict:
    """
    Ambil lirik lengkap dari lagu.
    mode: 'plain' atau 'synced'
    """
    fetch = _fetch(title)
    if not fetch["success"]:
        return fetch

    data = fetch["data"]
    item = _get_result(data, index)

    if not item:
        total = data["total"]
        return {"success": False, "message": f"❌ Pilihan tidak valid. Tersedia 1–{total} hasil."}

    if item.get("instrumental"):
        return {
            "success": False,
            "message": (
                f"🎹 **{item['title']}** oleh **{item['artist']}** adalah lagu instrumental.\n"
                f"Tidak ada lirik untuk lagu ini."
            )
        }

    lyrics_data = item.get("lyrics", {})
    lyrics_text = lyrics_data.get(mode) or lyrics_data.get("plain")

    if not lyrics_text:
        return {"success": False, "message": "❌ Lirik tidak tersedia untuk lagu ini."}

    duration = _format_duration(item.get("duration", 0))
    mode_label = "⏱️ Synced (dengan timestamp)" if mode == "synced" else "📝 Plain"

    # Potong lirik kalau terlalu panjang (batas Telegram ~4096 karakter)
    max_chars = 3000
    lirik_display = lyrics_text
    truncated = False
    if len(lyrics_text) > max_chars:
        lirik_display = lyrics_text[:max_chars]
        truncated = True

    message = (
        f"🎵 **{item['title']}**\n"
        f"👤 {item['artist']} — 💿 {item['album']}\n"
        f"⏱️ Durasi: {duration} | {mode_label}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{lirik_display}"
    )

    if truncated:
        message += "\n\n...\n*(lirik terpotong karena terlalu panjang)*"

    return {
        "success": True,
        "title": item["title"],
        "artist": item["artist"],
        "album": item["album"],
        "duration": duration,
        "lyrics": lyrics_text,
        "message": message
    }


# ==============================
# FUNGSI 3 — GET SONG INFO (tanpa lirik)
# ==============================

def get_song_info(title: str, index: int = 1) -> dict:
    """
    Ambil info lagu saja (judul, artis, album, durasi) tanpa lirik.
    """
    fetch = _fetch(title)
    if not fetch["success"]:
        return fetch

    data = fetch["data"]
    item = _get_result(data, index)

    if not item:
        total = data["total"]
        return {"success": False, "message": f"❌ Pilihan tidak valid. Tersedia 1–{total} hasil."}

    duration = _format_duration(item.get("duration", 0))
    instrumental = "🎹 Instrumental" if item.get("instrumental") else "🎤 Ada lirik"
    has_synced = "✅ Ada" if item.get("lyrics", {}).get("synced") else "❌ Tidak ada"

    message = (
        f"🎵 **Info Lagu**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎶 Judul: **{item['title']}**\n"
        f"👤 Artis: **{item['artist']}**\n"
        f"💿 Album: **{item['album']}**\n"
        f"⏱️ Durasi: **{duration}**\n"
        f"🎤 Tipe: {instrumental}\n"
        f"⏱️ Synced lyrics: {has_synced}\n"
        f"🆔 Song ID: {item.get('songId', '-')}"
    )

    return {
        "success": True,
        "title": item["title"],
        "artist": item["artist"],
        "album": item["album"],
        "duration": duration,
        "message": message
    }


# ==============================
# ROUTER — entry point OpenClaw
# ==============================

def run(function_name: str, params: dict) -> dict:
    """
    Entry point utama untuk OpenClaw.
    """
    functions = {
        "search_lyrics": lambda p: search_lyrics(p["title"]),
        "get_lyrics": lambda p: get_lyrics(p["title"], p.get("index", 1), p.get("mode", "plain")),
        "get_song_info": lambda p: get_song_info(p["title"], p.get("index", 1)),
    }

    if function_name not in functions:
        return {"success": False, "message": f"❌ Fungsi '{function_name}' tidak ditemukan."}

    return functions[function_name](params)


# ==============================
# TEST STANDALONE
# ==============================

if __name__ == "__main__":
    print("=== TEST LYRICS SKILL ===\n")

    # Test search
    result = search_lyrics("Obsessed")
    print(result["message"])

    print("\n" + "="*40 + "\n")

    # Test get lyrics hasil ke-1
    result2 = get_lyrics("Obsessed", index=1, mode="plain")
    print(result2["message"])

    print("\n" + "="*40 + "\n")

    # Test song info
    result3 = get_song_info("Obsessed", index=2)
    print(result3["message"])


# ==============================================================
# 📖 PANDUAN PEMAKAIAN UNTUK AI (BACA INI DULU!)
# ==============================================================
#
# Skill ini punya 3 fungsi utama. Berikut panduan lengkapnya:
#
# ──────────────────────────────────────────────────────────────
# 1️⃣  search_lyrics(title)
#     → Gunakan ini PERTAMA KALI saat user minta lirik lagu.
#     → Menampilkan DAFTAR semua lagu yang cocok dengan judul.
#     → Cocok untuk: "cariin lagu judulnya X", "ada lagu X gak?"
#
#     Contoh pemakaian:
#         search_lyrics("Espresso")
#         search_lyrics("Halu Feby Putri")
#         run("search_lyrics", {"title": "Espresso"})
#
#     Output penting:
#         result["message"]  → pesan siap kirim ke user
#         result["total"]    → jumlah lagu ditemukan
#         result["results"]  → list data mentah semua lagu
#
# ──────────────────────────────────────────────────────────────
# 2️⃣  get_lyrics(title, index=1, mode="plain")
#     → Gunakan ini saat user minta LIRIK LENGKAP sebuah lagu.
#     → Parameter index = nomor urut dari hasil search (mulai 1).
#     → Parameter mode:
#           "plain"  → lirik biasa tanpa timestamp (DEFAULT)
#           "synced" → lirik dengan timestamp [mm:ss.xx] tiap baris
#
#     Contoh pemakaian:
#         get_lyrics("Espresso")
#             → ambil lirik lagu pertama dari hasil pencarian "Espresso"
#
#         get_lyrics("Espresso", index=2)
#             → ambil lirik lagu ke-2 dari hasil pencarian
#
#         get_lyrics("Espresso", index=1, mode="synced")
#             → ambil lirik dengan timestamp (untuk karaoke/LRC)
#
#         run("get_lyrics", {"title": "Espresso", "index": 1, "mode": "plain"})
#             → cara panggil via router run()
#
#     Output penting:
#         result["message"]  → pesan siap kirim ke user (sudah diformat)
#         result["lyrics"]   → teks lirik mentah (belum diformat)
#         result["title"]    → judul lagu
#         result["artist"]   → nama artis
#         result["album"]    → nama album
#         result["duration"] → durasi format mm:ss
#
#     ⚠️  Catatan:
#         - Kalau lagu instrumental, tidak ada lirik, AI harus bilang ke user.
#         - Lirik > 3000 karakter akan otomatis dipotong di message,
#           tapi result["lyrics"] tetap berisi lirik penuh.
#
# ──────────────────────────────────────────────────────────────
# 3️⃣  get_song_info(title, index=1)
#     → Gunakan ini saat user hanya mau tahu INFO LAGU (tanpa lirik).
#     → Menampilkan: judul, artis, album, durasi, tipe, song ID.
#     → Cocok untuk: "info lagu X", "siapa penyanyi lagu X?"
#
#     Contoh pemakaian:
#         get_song_info("Halu")
#         get_song_info("Halu", index=2)
#         run("get_song_info", {"title": "Halu", "index": 1})
#
#     Output penting:
#         result["message"]  → pesan siap kirim ke user
#         result["title"]    → judul lagu
#         result["artist"]   → nama artis
#
# ──────────────────────────────────────────────────────────────
# 🔁  ALUR YANG DISARANKAN UNTUK AI:
#
#     User: "lirik lagu Espresso"
#       └─→ 1. Panggil search_lyrics("Espresso")
#           2. Kalau total == 1, langsung get_lyrics("Espresso", index=1)
#           3. Kalau total > 1, tunjukkan daftar dulu, tanya user mau yang mana
#           4. Setelah user pilih nomor, panggil get_lyrics(..., index=nomor)
#
#     User: "info lagu Halu"
#       └─→ Langsung panggil get_song_info("Halu")
#
#     User: "lirik synced / timestamp lagu X"
#       └─→ Panggil get_lyrics("X", mode="synced")
#
# ──────────────────────────────────────────────────────────────
# ❌  KALAU GAGAL:
#     Semua fungsi return dict dengan:
#         result["success"] == False
#         result["message"] == pesan error siap kirim ke user
#     AI tinggal kirim result["message"] langsung ke user.
#
# ==============================================================
