import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

def plot_thermowell_dimensions(pipe_id_mm, H, U, L):
    fig, ax = plt.subplots(figsize=(10, 3))

    # =========================
    # CENTERLINE
    # =========================
    ax.axhline(0, linestyle="--", linewidth=1)
    ax.text(-10, 0.05, "CL", fontsize=9)

    # =========================
    # PIPE (CÍRCULO)
    # =========================
    pipe_radius = pipe_id_mm / 2
    pipe = Circle((H + U/2, 0), pipe_radius, fill=False, linewidth=2)
    ax.add_patch(pipe)
    ax.text(H + U/2, pipe_radius + 5, "PIPE", ha="center")

    # =========================
    # NOZZLE
    # =========================
    nozzle_width = 20
    nozzle_height = pipe_radius + 20
    nozzle = Rectangle((H - nozzle_width/2, -nozzle_height/2),
                        nozzle_width, nozzle_height,
                        fill=False, linewidth=2)
    ax.add_patch(nozzle)
    ax.text(H, nozzle_height/2 + 5, "NOZZLE", ha="center")

    # =========================
    # TERMOWELL
    # =========================
    ax.plot([0, L], [0, 0], linewidth=6)
    ax.text(L + 5, 0, "TW", va="center")

    # =========================
    # FLANGE
    # =========================
    flange = Rectangle((H-5, -20), 10, 40, fill=False, linewidth=3)
    ax.add_patch(flange)
    ax.text(H, -25, "FLANGE", ha="center")

    # =========================
    # DIMENSIONS
    # =========================
    ax.annotate("", xy=(0, -40), xytext=(H, -40),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(H/2, -45, f"H = {H:.1f} mm", ha="center")

    ax.annotate("", xy=(H, -60), xytext=(H+U, -60),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(H + U/2, -65, f"U = {U:.1f} mm", ha="center")

    ax.annotate("", xy=(0, -80), xytext=(L, -80),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(L/2, -85, f"L = {L:.1f} mm", ha="center")

    # =========================
    # VIEW
    # =========================
    ax.set_aspect("equal", adjustable="box")
    ax.set_ylim(-100, pipe_radius + 60)
    ax.set_xlim(-20, L + 60)
    ax.axis("off")
    ax.set_title("Thermowell Installation Sketch")

    return fig
