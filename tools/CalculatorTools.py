"""
calculator_skill.py — All-in-one Calculator Hard Skill untuk OpenClaw
Tidak perlu install library eksternal, semua pake stdlib Python bawaan.
"""

import math
import cmath
import statistics


# ==============================
# SKILL MANIFEST
# ==============================

SKILL_MANIFEST = {
    "name": "calculator_hard",
    "version": "1.0.0",
    "description": "Kalkulator matematika tingkat lanjut — ekspresi bebas, statistik, matriks, kombinatorik, faktorisasi prima, konversi satuan.",
    "author": "Adit",
    "functions": [
        {
            "name": "calculate",
            "description": "Hitung ekspresi matematika dari teks. Mendukung +, -, *, /, ^, sqrt, sin, cos, log, dll.",
            "parameters": {
                "expression": {"type": "string", "description": "Ekspresi matematika, contoh: 'sqrt(144) + 3^2'"}
            }
        },
        {
            "name": "quadratic",
            "description": "Selesaikan persamaan kuadrat ax² + bx + c = 0",
            "parameters": {
                "a": {"type": "number", "description": "Koefisien a"},
                "b": {"type": "number", "description": "Koefisien b"},
                "c": {"type": "number", "description": "Koefisien c"}
            }
        },
        {
            "name": "statistics_calc",
            "description": "Hitung statistik lengkap dari list angka (mean, median, modus, std deviasi, variansi, dll).",
            "parameters": {
                "numbers": {"type": "array", "description": "List angka, contoh: [10, 20, 30, 40, 50]"}
            }
        },
        {
            "name": "convert_unit",
            "description": "Konversi satuan panjang, berat, suhu, dan kecepatan.",
            "parameters": {
                "value": {"type": "number", "description": "Nilai yang mau dikonversi"},
                "from_unit": {"type": "string", "description": "Satuan asal, contoh: 'km'"},
                "to_unit": {"type": "string", "description": "Satuan tujuan, contoh: 'mile'"}
            }
        },
        {
            "name": "combinatorics",
            "description": "Hitung permutasi P(n,r) dan kombinasi C(n,r).",
            "parameters": {
                "n": {"type": "integer", "description": "Total elemen"},
                "r": {"type": "integer", "description": "Elemen yang dipilih"},
                "mode": {"type": "string", "description": "'permutation', 'combination', atau 'both'", "default": "both"}
            }
        },
        {
            "name": "prime_factorization",
            "description": "Faktorisasi prima dari sebuah bilangan bulat.",
            "parameters": {
                "n": {"type": "integer", "description": "Bilangan yang mau difaktorisasi"}
            }
        },
        {
            "name": "is_prime",
            "description": "Cek apakah sebuah bilangan adalah bilangan prima.",
            "parameters": {
                "n": {"type": "integer", "description": "Bilangan yang dicek"}
            }
        },
        {
            "name": "matrix_ops",
            "description": "Operasi matriks 2x2 atau 3x3: penjumlahan, pengurangan, perkalian, determinan.",
            "parameters": {
                "A": {"type": "array", "description": "Matriks A (list of list)"},
                "B": {"type": "array", "description": "Matriks B (list of list), kosong [] jika cuma determinan"},
                "operation": {"type": "string", "description": "'add', 'subtract', 'multiply', atau 'determinant'", "default": "add"}
            }
        }
    ]
}


# ==============================
# HELPER
# ==============================

def get_weather_emoji(condition: str) -> str:
    pass  # placeholder biar ga error kalau diimport bareng weather_tool


def _format_matrix(matrix: list) -> str:
    return "\n".join(["  " + str(row) for row in matrix])


# ==============================
# FUNGSI 1 — CALCULATE
# ==============================

def calculate(expression: str) -> dict:
    """
    Hitung ekspresi matematika dari teks.
    Contoh: "sqrt(144) + 3^2", "sin(90)", "log(1000)"
    """
    try:
        expr = expression.replace("^", "**").replace("×", "*").replace("÷", "/").replace("√", "sqrt")
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
        allowed.update({"abs": abs, "round": round, "int": int, "float": float})
        result = eval(expr, {"__builtins__": {}}, allowed)
        return {
            "success": True,
            "expression": expression,
            "result": result,
            "message": f"✅ `{expression}` = **{result}**"
        }
    except ZeroDivisionError:
        return {"success": False, "message": "❌ Tidak bisa bagi dengan nol!"}
    except Exception as e:
        return {"success": False, "message": f"❌ Ekspresi tidak valid: {str(e)}"}


# ==============================
# FUNGSI 2 — QUADRATIC
# ==============================

def quadratic(a: float, b: float, c: float) -> dict:
    """
    Selesaikan persamaan kuadrat ax² + bx + c = 0
    """
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        msg = (
            f"📐 **Persamaan Kuadrat: {a}x² + {b}x + {c} = 0**\n"
            f"Diskriminan: {discriminant} (2 akar real)\n"
            f"x₁ = **{round(x1, 6)}**\n"
            f"x₂ = **{round(x2, 6)}**"
        )
        return {"success": True, "x1": x1, "x2": x2, "discriminant": discriminant, "message": msg}
    elif discriminant == 0:
        x = -b / (2*a)
        msg = (
            f"📐 **Persamaan Kuadrat: {a}x² + {b}x + {c} = 0**\n"
            f"Diskriminan: 0 (1 akar kembar)\n"
            f"x = **{round(x, 6)}**"
        )
        return {"success": True, "x1": x, "x2": x, "discriminant": 0, "message": msg}
    else:
        r1 = (-b + cmath.sqrt(discriminant)) / (2*a)
        r2 = (-b - cmath.sqrt(discriminant)) / (2*a)
        msg = (
            f"📐 **Persamaan Kuadrat: {a}x² + {b}x + {c} = 0**\n"
            f"Diskriminan: {discriminant} (akar kompleks)\n"
            f"x₁ = **{r1}**\n"
            f"x₂ = **{r2}**"
        )
        return {"success": True, "x1": str(r1), "x2": str(r2), "discriminant": discriminant, "message": msg}


# ==============================
# FUNGSI 3 — STATISTIK
# ==============================

def statistics_calc(numbers: list) -> dict:
    """
    Hitung statistik lengkap dari list angka.
    """
    try:
        n = len(numbers)
        mean = statistics.mean(numbers)
        median = statistics.median(numbers)
        mode_val = statistics.mode(numbers) if n > 1 else numbers[0]
        std_dev = statistics.stdev(numbers) if n > 1 else 0
        variance = statistics.variance(numbers) if n > 1 else 0
        total = sum(numbers)
        minimum = min(numbers)
        maximum = max(numbers)
        range_val = maximum - minimum

        msg = (
            f"📊 **Statistik Data**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Data: {numbers}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔢 Jumlah data (n): {n}\n"
            f"➕ Total: {total}\n"
            f"📈 Mean: **{round(mean, 4)}**\n"
            f"📍 Median: **{median}**\n"
            f"🎯 Modus: **{mode_val}**\n"
            f"📉 Std Deviasi: **{round(std_dev, 4)}**\n"
            f"📦 Variansi: **{round(variance, 4)}**\n"
            f"🔼 Maks: **{maximum}**  🔽 Min: **{minimum}**\n"
            f"↔️ Range: **{range_val}**"
        )
        return {"success": True, "mean": mean, "median": median, "std_dev": std_dev, "message": msg}
    except Exception as e:
        return {"success": False, "message": f"❌ Error: {str(e)}"}


# ==============================
# FUNGSI 4 — KONVERSI SATUAN
# ==============================

def convert_unit(value: float, from_unit: str, to_unit: str) -> dict:
    """
    Konversi satuan panjang, berat, suhu, dan kecepatan.
    """
    conversions = {
        "km": 1000, "m": 1, "cm": 0.01, "mm": 0.001,
        "mile": 1609.34, "yard": 0.9144, "ft": 0.3048, "inch": 0.0254,
        "kg": 1000, "g": 1, "mg": 0.001, "lb": 453.592, "oz": 28.3495, "ton": 1_000_000,
        "m/s": 1, "km/h": 0.27778, "mph": 0.44704, "knot": 0.514444,
    }
    fu, tu = from_unit.lower(), to_unit.lower()

    temp_units = {"c", "f", "k"}
    if fu in temp_units and tu in temp_units:
        if fu == "c":
            result = value * 9/5 + 32 if tu == "f" else value + 273.15 if tu == "k" else value
        elif fu == "f":
            result = (value - 32) * 5/9 if tu == "c" else (value - 32) * 5/9 + 273.15 if tu == "k" else value
        elif fu == "k":
            result = value - 273.15 if tu == "c" else (value - 273.15) * 9/5 + 32 if tu == "f" else value
        return {"success": True, "message": f"🌡️ **{value}°{fu.upper()}** = **{round(result, 4)}°{tu.upper()}**"}

    if fu not in conversions or tu not in conversions:
        return {"success": False, "message": f"❌ Satuan '{from_unit}' atau '{to_unit}' tidak dikenal."}

    result = value * conversions[fu] / conversions[tu]
    return {"success": True, "result": result, "message": f"📏 **{value} {from_unit}** = **{round(result, 6)} {to_unit}**"}


# ==============================
# FUNGSI 5 — KOMBINATORIK
# ==============================

def combinatorics(n: int, r: int, mode: str = "both") -> dict:
    """
    Hitung permutasi P(n,r) dan/atau kombinasi C(n,r).
    """
    try:
        perm = math.perm(n, r)
        comb = math.comb(n, r)
        if mode == "permutation":
            msg = f"🔀 **P({n},{r})** = **{perm}**"
        elif mode == "combination":
            msg = f"🎲 **C({n},{r})** = **{comb}**"
        else:
            msg = f"🧮 **Kombinatorik n={n}, r={r}**\n🔀 Permutasi P({n},{r}) = **{perm}**\n🎲 Kombinasi C({n},{r}) = **{comb}**"
        return {"success": True, "permutation": perm, "combination": comb, "message": msg}
    except Exception as e:
        return {"success": False, "message": f"❌ Error: {str(e)}"}


# ==============================
# FUNGSI 6 — FAKTORISASI PRIMA
# ==============================

def prime_factorization(n: int) -> dict:
    """
    Faktorisasi prima dari bilangan n.
    """
    if n < 2:
        return {"success": False, "message": "❌ Masukkan bilangan >= 2"}
    factors, temp, d = [], n, 2
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    is_prime_val = len(factors) == 1 and factors[0] == n
    msg = (
        f"🔢 **Faktorisasi Prima: {n}**\n"
        f"= {' × '.join(map(str, factors))}\n"
        f"{'✅ Bilangan Prima!' if is_prime_val else '📦 Bilangan Komposit'}"
    )
    return {"success": True, "factors": factors, "is_prime": is_prime_val, "message": msg}


# ==============================
# FUNGSI 7 — CEK PRIMA
# ==============================

def is_prime(n: int) -> dict:
    """
    Cek apakah n adalah bilangan prima.
    """
    if n < 2:
        return {"success": True, "result": False, "message": f"❌ {n} bukan bilangan prima."}
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return {"success": True, "result": False, "message": f"❌ **{n}** bukan prima. Faktor: {i} × {n//i}"}
    return {"success": True, "result": True, "message": f"✅ **{n}** adalah bilangan prima!"}


# ==============================
# FUNGSI 8 — MATRIKS
# ==============================

def matrix_ops(A: list, B: list = None, operation: str = "add") -> dict:
    """
    Operasi matriks 2x2 atau 3x3: add, subtract, multiply, determinant.
    """
    try:
        rows = len(A)
        if operation == "determinant":
            if rows == 2:
                det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
            elif rows == 3:
                det = (
                    A[0][0]*(A[1][1]*A[2][2] - A[1][2]*A[2][1]) -
                    A[0][1]*(A[1][0]*A[2][2] - A[1][2]*A[2][0]) +
                    A[0][2]*(A[1][0]*A[2][1] - A[1][1]*A[2][0])
                )
            else:
                return {"success": False, "message": "❌ Hanya support matriks 2x2 atau 3x3"}
            return {"success": True, "result": det, "message": f"🟦 **det(A)** = **{det}**"}

        B = B or []
        result = []
        if operation == "multiply":
            cols_B = len(B[0])
            for i in range(rows):
                row = [sum(A[i][k] * B[k][j] for k in range(rows)) for j in range(cols_B)]
                result.append(row)
        else:
            for i in range(rows):
                row = [A[i][j] + B[i][j] if operation == "add" else A[i][j] - B[i][j] for j in range(len(A[i]))]
                result.append(row)

        return {
            "success": True,
            "result": result,
            "message": f"🟦 **Hasil Matriks ({operation}):**\n{_format_matrix(result)}"
        }
    except Exception as e:
        return {"success": False, "message": f"❌ Error: {str(e)}"}


# ==============================
# ROUTER — dipanggil OpenClaw
# ==============================

def run(function_name: str, params: dict) -> dict:
    """
    Entry point utama untuk OpenClaw.
    OpenClaw manggil fungsi ini dengan nama fungsi + parameternya.
    """
    functions = {
        "calculate": lambda p: calculate(p["expression"]),
        "quadratic": lambda p: quadratic(p["a"], p["b"], p["c"]),
        "statistics_calc": lambda p: statistics_calc(p["numbers"]),
        "convert_unit": lambda p: convert_unit(p["value"], p["from_unit"], p["to_unit"]),
        "combinatorics": lambda p: combinatorics(p["n"], p["r"], p.get("mode", "both")),
        "prime_factorization": lambda p: prime_factorization(p["n"]),
        "is_prime": lambda p: is_prime(p["n"]),
        "matrix_ops": lambda p: matrix_ops(p["A"], p.get("B", []), p.get("operation", "add")),
    }

    if function_name not in functions:
        return {"success": False, "message": f"❌ Fungsi '{function_name}' tidak ditemukan."}

    return functions[function_name](params)


# ==============================
# TEST STANDALONE
# ==============================

if __name__ == "__main__":
    print(calculate("sqrt(144) + 3^3")["message"])
    print(quadratic(1, -5, 6)["message"])
    print(statistics_calc([10, 20, 30, 40, 50, 60])["message"])
    print(convert_unit(100, "km", "mile")["message"])
    print(convert_unit(100, "c", "f")["message"])
    print(combinatorics(10, 3)["message"])
    print(prime_factorization(360)["message"])
    print(is_prime(97)["message"])
    print(matrix_ops([[1,2],[3,4]], [], "determinant")["message"])

    # Test via router
    print("\n--- Test via run() router ---")
    print(run("calculate", {"expression": "2^10"})["message"])
    print(run("is_prime", {"n": 13})["message"])
