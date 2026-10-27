# II laboratorinis darbas, variantas 9

Paprastosios diferencialinės lygties pradinio uždavinio skaitinis sprendimas:

u' = x² cos(u − x), u(0) = 0, 0 ≤ x ≤ 1.

Metodai: 4-pakopis Rungės–Kuto (p = 4) ir dvipakopis Rungės–Kuto su σ = 0.5
(prediktorius–korektorius, p = 2), žingsniai 0.1 ir 0.05. Paklaida įvertinta Rungės metodu,
palyginta su `scipy.integrate.solve_ivp` (RK45).

## Failai

| Failas | Kas tai |
|---|---|
| `lab2_var9.py` | programa (parametrai keičiami failo viršuje) |
| `ataskaita.tex` / `ataskaita.pdf` | ataskaita |
| `fig_*.png` | grafikai |
| `output.txt` | programos išvestis (lentelės) |
| `make_docx.py` | `ataskaita.tex` → `ataskaita.docx` |

## Paleidimas

```
pip install numpy scipy matplotlib
python lab2_var9.py
```
