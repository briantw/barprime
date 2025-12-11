from matplotlib.animation import PillowWriter
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------------------
# Config
# -----------------------------------
N_START = 2      # first integer to show
N_END   = 256    # last integer to show

# Primes on the x-axis, left to right (largest → smallest)
PRIMES = [
      2,   3,   5,   7,  11,  13,  17,  19,
     23,  29,  31,  37,  41,  43,  47,  53,
     59,  61,  67,  71,  73,  79,  83,  89,
     97, 101, 103, 107, 109, 113, 127, 131,
    137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197, 199, 211, 223,
    227, 229, 233, 239, 241, 251
]


# -----------------------------------
# Helpers
# -----------------------------------
def factor_exponents_in_fixed_primes(n, primes):
    """
    Return a list of exponents of each prime in 'primes' for n.
    We only factor using these primes; if n has larger prime factors,
    they are ignored (bars stay at 0).
    """
    exps = []
    temp = n
    for p in primes:
        e = 0
        while temp % p == 0:
            temp //= p
            e += 1
        exps.append(e)
    return exps

def factor_string(n, primes):
    """
    Return a nicely formatted prime factorisation string with superscripts.
    Example: 20 -> '5 × 2²'
    """
    temp = n
    parts = []
    # superscripts for small exponents (enough for n <= 255)
    supers = {0:"⁰", 1:"", 2:"²", 3:"³", 4:"⁴",
              5:"⁵", 6:"⁶", 7:"⁷", 8:"⁸", 9:"⁹"}

    for p in primes:
        if temp == 1:
            break
        exp = 0
        while temp % p == 0:
            temp //= p
            exp += 1
        if exp > 0:
            if exp == 1:
                parts.append(f"{p}")
            else:
                parts.append(f"{p}{supers[exp]}")
    if not parts:
        # n is 1 or has a prime > max(PRIMES); for 2..255 this shouldn't happen
        return str(n)
    return " × ".join(parts)

# Precompute max exponent for y-scale
max_exp = 0
for n in range(N_START, N_END + 1):
    exps = factor_exponents_in_fixed_primes(n, PRIMES)
    max_exp = max(max_exp, max(exps))

if max_exp == 0:
    max_exp = 1

# -----------------------------------
# Matplotlib setup
# -----------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))

x_pos = list(range(len(PRIMES)))
initial_heights = [0] * len(PRIMES)
bars = ax.bar(x_pos, initial_heights)

ax.set_xticks(x_pos)
ax.set_xticklabels(PRIMES, rotation=90)
ax.set_ylim(0, max_exp + 0.5)
ax.set_xlabel("Prime")
ax.set_ylabel("Exponent")
title = ax.set_title("n = ?")

# factorisation text, centred at top of axes
fact_text = ax.text(
    0.4, 0.92, "",               # <-- move it near the left edge
    ha='left', va='center',       # <-- left-justify it
    transform=ax.transAxes,
    fontsize=12
)


plt.tight_layout()

# -----------------------------------
# Animation update function
# -----------------------------------
def update(frame_index):
    n = N_START + frame_index
    exps = factor_exponents_in_fixed_primes(n, PRIMES)

    for rect, h in zip(bars, exps):
        rect.set_height(h)

    title.set_text(f"n = {n}")
    fact_text.set_text(f"{n} = {factor_string(n, PRIMES)}")

    return bars

num_frames = N_END - N_START + 1

anim = FuncAnimation(
    fig,
    update,
    frames=num_frames,
    interval=5,   # 1 second per frame; change if you want faster
    blit=False,
    repeat=False
)

writer = PillowWriter(fps=1)   # 1 frame per second (matches your animation)
anim.save("primebars.gif", writer=writer)
plt.show()
