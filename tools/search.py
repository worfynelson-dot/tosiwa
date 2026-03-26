# tools/search.py
# DuckDuckGo Search Tool — drop in /tools to auto-load

from duckduckgo_search import DDGS

# ── Tool Definition (wajib ada di setiap tool file) ──────────────────────────
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "search_internet",
        "description": (
            "Cari informasi di internet menggunakan DuckDuckGo. "
            "Gunakan ini ketika user minta cari sesuatu di internet, "
            "butuh info terbaru, atau perlu referensi dari web."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Kata kunci yang mau dicari"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Jumlah hasil maksimal (default: 5)"
                }
            },
            "required": ["query"]
        }
    }
}

# ── Tool Handler (wajib ada, nama fungsi = nama tool di TOOL_DEFINITION) ─────
def search_internet(query: str, max_results: int = 5) -> str:
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(
                    f"📌 {r['title']}\n"
                    f"🔗 {r['href']}\n"
                    f"📝 {r['body']}\n"
                )
        if not results:
            return "Tidak ada hasil ditemukan."
        return f"🔍 Hasil pencarian untuk '{query}':\n\n" + "\n---\n".join(results)
    except Exception as e:
        return f"❌ Error saat search: {str(e)}"
