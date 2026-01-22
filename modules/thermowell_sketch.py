import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

def plot_thermowell_datasheet(pipe_id_mm, H, U, L):
    fig, ax = plt.subplots(figsize=(4, 10))

    # =========================
    # PIPE
    # =========================
    pipe_radius = pipe_id_mm / 2
    pipe_center_y = 0

    pipe = Circle((0, pipe_center_y), pipe_radius, fill=False, linewidth=2)
    ax.add_patch(pipe)

    # =========================
    # CENTERLINE
    # =========================
    ax.axhline(pipe_radius-pipe_id_mm*2/3, linestyle="--", linewidth=1)

    # =========================
    # NOZZLE (desde OD del pipe)
    # =========================
    nozzle_width = 20
    nozzle_height = H

    nozzle = Rectangle(
        (-nozzle_width/2, pipe_radius),
        nozzle_width,
        nozzle_height,
        fill=False,
        linewidth=2
    )
    ax.add_patch(nozzle)
  

    # =========================
    # FLANGE
    # =========================
    flange_width = 80
    flange_height = 15

    flange = Rectangle(
        (-flange_width/2, pipe_radius + nozzle_height-flange_height),
        flange_width,
        flange_height,
        fill=False,
        linewidth=3
    )
    ax.add_patch(flange)
 

    # =========================
    # THERMOWELL (ENTRA AL PIPE)
    # =========================
    tw_start = pipe_radius + nozzle_height
    tw_end = -U   # entra hasta U desde CL

    ax.plot([0, 0], [tw_start, tw_end], linewidth=6, color="blue")
   

    # =========================
    # DIMENSIONS
    # =========================
    # H
    ax.annotate("", xy=(-50, pipe_radius), xytext=(-50, pipe_radius + H),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(-55, pipe_radius + H/2, f"H = {H:.1f} mm", rotation=90, va="center", fontsize=8)

    # U
    ax.annotate("", xy=(-10, -U), xytext=(-10, pipe_radius),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(-20, -U/2, f"U = {U:.1f} mm", rotation=90, va="center", fontsize=8)

    # L
    ax.annotate("", xy=(50, tw_start), xytext=(50, tw_end),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(55, (tw_start + tw_end)/2, f"L = {L:.1f} mm", rotation=90, va="center", fontsize=8)

    # =========================
    # VIEW
    # =========================
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-pipe_radius-20, pipe_radius+20)
    ax.set_ylim(-pipe_radius - U - 40, tw_start + 40)
    ax.axis("off")
    ax.set_title("Vertical Thermowell – Datasheet Style", fontsize=10)

    return fig
