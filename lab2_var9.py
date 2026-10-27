# Edvin Katenel
# II laboratorinis darbas, variantas 9
# Koši uždavinys: u' = f(x, u), u(X0) = U0, X0 <= x <= X1
# Metodai: 4-pakopis Rungės-Kuto (p = 4) ir dvipakopis RK su parametru sigma (p = 2)
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

sys.stdout.reconfigure(encoding='utf-8')   # lietuviškos raidės Windows terminale
os.chdir(os.path.dirname(os.path.abspath(__file__)))   # paveikslai saugomi šalia programos

#parametrai
def f(x, u):
    return x**2 * np.cos(u - x)

F_TEKSTAS = r"$x^2\cos(u-x)$"    # funkcija grafikų pavadinimams
X0, X1 = 0.0, 1.0                # intervalas [X0; X1]
U0 = 0.0                         # pradinė sąlyga u(X0) = U0
TAU = 0.05                       # mažesnis žingsnis; didesnis bus 2*TAU
SIGMA = 0.5                      # dvipakopio metodo parametras
RODYTI = True
#


def rk4(f, x0, u0, x1, tau):
    """Klasikinis 4-pakopis Rungės-Kuto metodas."""
    n = int(round((x1 - x0) / tau))
    x = x0 + tau * np.arange(n + 1)
    y = np.empty(n + 1); y[0] = u0
    for i in range(n):
        k1 = f(x[i], y[i])
        k2 = f(x[i] + tau / 2, y[i] + tau / 2 * k1)
        k3 = f(x[i] + tau / 2, y[i] + tau / 2 * k2)
        k4 = f(x[i] + tau, y[i] + tau * k3)
        y[i + 1] = y[i] + tau / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return x, y


def rk2(f, x0, u0, x1, tau, sigma=0.5):
    """Dvipakopis Rungės-Kuto metodas:
    y_{i+1} = y_i + tau*((1-sigma)*k1 + sigma*k2),
    k1 = f(x_i, y_i),  k2 = f(x_i + a*tau, y_i + a*tau*k1),  a = 1/(2*sigma).
    Kai sigma = 0.5 (a = 1) - Hojno (prediktoriaus-korektoriaus) metodas."""
    a = 1 / (2 * sigma)
    n = int(round((x1 - x0) / tau))
    x = x0 + tau * np.arange(n + 1)
    y = np.empty(n + 1); y[0] = u0
    for i in range(n):
        k1 = f(x[i], y[i])
        k2 = f(x[i] + a * tau, y[i] + a * tau * k1)
        y[i + 1] = y[i] + tau * ((1 - sigma) * k1 + sigma * k2)
    return x, y


#skaičiavimai 
T1, T2 = 2 * TAU, TAU            # žingsniai 2*tau ir tau
assert abs((X1 - X0) / T1 - round((X1 - X0) / T1)) < 1e-9, "intervalo ilgis turi dalintis iš 2*TAU"

res = {}
for tau in (T1, T2):
    res[('RK4', tau)] = rk4(f, X0, U0, X1, tau)
    res[('RK2', tau)] = rk2(f, X0, U0, X1, tau, sigma=SIGMA)

#
ref = solve_ivp(f, (X0, X1), [U0], method='RK45', rtol=1e-12, atol=1e-14, dense_output=True)
u_ref = lambda x: ref.sol(x)[0]

p = {'RK4': 4, 'RK2': 2}
xg = res[('RK4', T1)][0]

print(f"Reikšmės tinklo taškuose (u({X0:g}) = {U0:g})")
print(f"{'x':>6} | {'RK4 '+str(T1):>12} {'RK4 '+str(T2):>12} | {'RK2 '+str(T1):>12} {'RK2 '+str(T2):>12} | {'solve_ivp':>12}")
for k, xv in enumerate(xg):
    print(f"{xv:6.2f} | {res[('RK4',T1)][1][k]:12.8f} {res[('RK4',T2)][1][2*k]:12.8f} | "
          f"{res[('RK2',T1)][1][k]:12.8f} {res[('RK2',T2)][1][2*k]:12.8f} | {u_ref(xv):12.8f}")

print(f"\nPaklaidos įvertis Rungės metodu |y_2tau - y_tau| / (2^p - 1), tau = {T2:g}")
print(f"{'x':>6} | {'RK4 įvertis':>12} {'RK4 tikroji':>12} | {'RK2 įvertis':>12} {'RK2 tikroji':>12}")
runge = {}
for m in ('RK4', 'RK2'):
    y2t = res[(m, T1)][1]           # žingsnis 2*tau
    yt = res[(m, T2)][1][::2]       # žingsnis tau tuose pačiuose taškuose
    runge[m] = (np.abs(y2t - yt) / (2**p[m] - 1), np.abs(u_ref(xg) - yt))
for k in range(1, len(xg)):
    print(f"{xg[k]:6.2f} | {runge['RK4'][0][k]:12.3e} {runge['RK4'][1][k]:12.3e} | "
          f"{runge['RK2'][0][k]:12.3e} {runge['RK2'][1][k]:12.3e}")
for m in ('RK4', 'RK2'):
    print(f"{m}: max Rungės įvertis ({X0:g};{X1:g}] = {runge[m][0][1:].max():.3e}, "
          f"max tikroji paklaida = {runge[m][1][1:].max():.3e}")

#
for m in ('RK4', 'RK2'):
    e1 = abs(res[(m, T1)][1][-1] - u_ref(X1))
    e2 = abs(res[(m, T2)][1][-1] - u_ref(X1))
    print(f"{m}: paklaida x={X1:g}: tau={T1:g} -> {e1:.3e}, tau={T2:g} -> {e2:.3e}, "
          f"santykis {e1/e2:.2f} (2^p = {2**p[m]})")

# grafikai 
plt.rcParams.update({"font.size": 11})
xx = np.linspace(X0, X1, 400)
names = {'RK4': '4-pakopis RK', 'RK2': rf'dvipakopis RK ($\sigma={SIGMA:g}$)'}


def two_panel(title, curves, fname):
    """Viršuje - sprendiniai, apačioje - |y - u_ref| logaritminėje skalėje."""
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7, 7), sharex=True,
                                 gridspec_kw={'height_ratios': [3, 2]})
    a1.plot(xx, u_ref(xx), 'k-', lw=2.5, alpha=.35, label='solve_ivp (RK45)')
    for (x, y, lab, st) in curves:
        a1.plot(x, y, st, ms=5, lw=1.2, label=lab)
        a2.semilogy(x[1:], np.abs(y[1:] - u_ref(x[1:])), st, ms=5, lw=1.2, label=lab)
    a1.set_title(f"$u'=${F_TEKSTAS}, $u({X0:g})={U0:g}$\n" + title, fontsize=11)
    a1.set_ylabel('$u(x)$'); a1.grid(alpha=.3); a1.legend(fontsize=9)
    a2.set_xlabel('$x$'); a2.set_ylabel(r'$|y_i-u(x_i)|$'); a2.grid(alpha=.3, which='both')
    a2.legend(fontsize=9)
    fig.tight_layout(); fig.savefig(fname, dpi=200)
    print("Išsaugota:", os.path.abspath(fname))


for m, fn in (('RK4', 'fig_a_rk4.png'), ('RK2', 'fig_a_rk2.png')):
    two_panel(names[m] + f': žingsniai {T1:g} ir {T2:g}',
              [(*res[(m, T1)], rf'$\tau={T1:g}$', 'o--'), (*res[(m, T2)], rf'$\tau={T2:g}$', 's-')], fn)

for tau, fn in ((T1, 'fig_b_2tau.png'), (T2, 'fig_b_tau.png')):
    two_panel(rf'$\tau={tau:g}$: 4-pakopis RK ir dvipakopis RK ($\sigma={SIGMA:g}$)',
              [(*res[('RK4', tau)], names['RK4'], 'o--'), (*res[('RK2', tau)], names['RK2'], 's-')], fn)

if RODYTI:
    plt.show()
