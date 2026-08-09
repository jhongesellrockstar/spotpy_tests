"""Generate the two workflow figures used by Markdown and LaTeX manuals."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)
BLUE, GREEN, ORANGE, GREY = "#176B87", "#4C956C", "#E07A5F", "#34495E"

def box(ax, xy, text, color=BLUE, width=2.5, height=.62, fontsize=9):
    x, y = xy
    patch = FancyBboxPatch((x-width/2, y-height/2), width, height, boxstyle="round,pad=0.04", fc=color, ec="white", lw=1.5)
    ax.add_patch(patch); ax.text(x, y, text, color="white", ha="center", va="center", fontsize=fontsize, weight="bold")
def arrow(ax, start, end, label=None, color=GREY):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13, color=color, lw=1.5, connectionstyle="arc3,rad=0.0"))
    if label: ax.text((start[0]+end[0])/2, (start[1]+end[1])/2+.12, label, ha="center", va="bottom", fontsize=8, color=color)
def save(fig, stem):
    fig.savefig(OUT/f"{stem}.png", dpi=220, bbox_inches="tight"); fig.savefig(OUT/f"{stem}.pdf", bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6)); ax.set(xlim=(0,10), ylim=(0,7)); ax.axis("off")
box(ax,(1.6,6.2),"DATOS",GREEN); box(ax,(1.6,5.0),"PREPROCESAMIENTO",GREEN); box(ax,(4.9,4.0),"MODELO",BLUE)
box(ax,(8.3,5.3),"SPOTPY ALGORITHM",ORANGE); box(ax,(8.3,4.0),"PARÁMETROS",ORANGE); box(ax,(4.9,2.7),"SIMULACIÓN",BLUE)
box(ax,(1.6,1.3),"OBSERVACIÓN",GREEN); box(ax,(4.9,1.3),"OBJECTIVE",ORANGE)
arrow(ax,(1.6,5.87),(1.6,5.34)); arrow(ax,(2.85,5.0),(4.1,4.15),"forcing"); arrow(ax,(8.3,4.97),(8.3,4.34),"parameters()")
arrow(ax,(7.05,4.0),(6.17,4.0),"vector"); arrow(ax,(4.9,3.67),(4.9,3.04),"simulation()")
arrow(ax,(1.6,1.63),(3.65,1.35),"evaluation()"); arrow(ax,(4.9,2.37),(4.9,1.64)); arrow(ax,(6.15,1.3),(7.8,4.95),"objectivefunction()")
ax.set_title("Flujo operativo del laboratorio SPOTPY", fontsize=16, weight="bold", pad=12); save(fig,"spotpy_workflow")

fig, ax = plt.subplots(figsize=(7.2, 8.2)); ax.set(xlim=(0,7.2), ylim=(0,10)); ax.axis("off")
labels=[("SPOTPY",9.3,ORANGE),("parameter set",8.25,ORANGE),("parameter_writer",7.2,BLUE),("copia aislada del proyecto SWAT+",6.15,BLUE),("swatplus.exe",5.1,GREY),("output_parser",4.05,BLUE),("Q simulada [m³/s] (futuro)",3.0,GREEN),("objective function",1.85,ORANGE),("SPOTPY: siguiente conjunto",.7,ORANGE)]
for text_,y,c in labels: box(ax,(3.6,y),text_,c,width=4.4)
for (_,y1,_),(_,y2,_) in zip(labels,labels[1:]): arrow(ax,(3.6,y1-.34),(3.6,y2+.34))
box(ax,(6.1,1.85),"Q observada\n[m³/s]\n(futura)",GREEN,width=1.7,height=.9,fontsize=7.5); arrow(ax,(5.23,1.85),(4.87,1.85))
ax.text(3.6,9.85,"SPOTPY + futuro SWAT+ IGP",ha="center",fontsize=16,weight="bold"); ax.text(3.6,.08,"Arquitectura propuesta: el output real de SWAT+ aún no está implementado.",ha="center",fontsize=8,color=GREY)
save(fig,"spotpy_swatplus_workflow")
print("FIGURES_OK", OUT)
