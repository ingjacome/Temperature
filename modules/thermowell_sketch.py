import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

def plot_thermowell_datasheet(pipe_id_mm, H, U, L,pipe_od, connection_value):
    fig, ax = plt.subplots(figsize=(4, 10))

    # =========================
    # PIPE
    # =========================
    pipe_radius = pipe_id_mm / 2
    pipe_radius_od = pipe_od / 2
    pipe_center_y = 0

    pipe = Circle((0, pipe_center_y), pipe_radius, fill=False, linewidth=2)
    ax.add_patch(pipe)
    pipe1 = Circle((0, pipe_center_y), pipe_radius_od, fill=False, linewidth=2)
    ax.add_patch(pipe1)
    # =========================
    # CENTERLINE
    # =========================
    ax.axhline(pipe_radius-pipe_id_mm*2/3, linestyle="--", linewidth=1)

    # =========================
    # NOZZLE (desde OD del pipe)
    # =========================
    nozzle_width = connection_value*25.4
    nozzle_height = H

    nozzle = Rectangle(
        (-nozzle_width/2, pipe_radius_od),
        nozzle_width,
        nozzle_height,
        fill=False,
        linewidth=2
    )
    ax.add_patch(nozzle)
  

    # =========================
    # FLANGE
    # =========================
    flange_width = connection_value*25.4*2
    flange_height = 15

    flange = Rectangle(
        (-flange_width/2, pipe_radius_od + nozzle_height-flange_height),
        flange_width,
        flange_height,
        fill=False,
        linewidth=3
    )
    ax.add_patch(flange)
 

    # =========================
    # THERMOWELL (ENTRA AL PIPE)
    # =========================
    tw_start = pipe_radius_od + nozzle_height
    tw_end = pipe_radius-pipe_id_mm*2/3   # entra hasta U desde CL

    ax.plot([0, 0], [tw_start, tw_end], linewidth=4, color="red")
   

    # =========================
    # DIMENSIONS
    # =========================
    # H
    ax.annotate("", xy=(-pipe_radius/4-pipe_radius/12, pipe_radius_od), xytext=(-pipe_radius/4-pipe_radius/12, pipe_radius_od + H),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(-pipe_radius/4-pipe_radius/8, pipe_radius_od + H/2, f"H = {H:.1f} mm", rotation=90, va="center", fontsize=8)

    # U
    ax.annotate("", xy=(-pipe_radius/15, pipe_radius), xytext=(-pipe_radius/15, tw_end),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(-pipe_radius/6, (pipe_radius + tw_end)/2, f"U = {U:.1f} mm", rotation=90, va="center", fontsize=8)

    # L
    ax.annotate("", xy=(pipe_radius_od + pipe_radius_od/50, tw_start), xytext=(pipe_radius_od + pipe_radius_od/50, tw_end),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(pipe_radius_od + pipe_radius_od/30, (tw_start + tw_end)/2, f"L = {L:.1f} mm", rotation=90, va="center", fontsize=8)

    # =========================
    # VIEW
    # =========================
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-pipe_radius - 30, pipe_radius + 30)
    ax.set_ylim(-pipe_radius - 30, tw_start + 30)
    ax.axis("off")
    ax.set_title("Vertical Thermowell – Datasheet Style", fontsize=10)

    return fig
