"""Overall architecture / experimental-design figure for the thesis -> Report/figures/fig_architecture.png

Three bands: toolkits (Lexsi stack + llama.cpp), the six-stage pipeline with the RQ chain, and the two machines
with the hand-off links. Drawn with matplotlib only; no data needed. Boxes are spaced so that every arrow is
visible between them and no connector crosses text.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Report/figures/fig_architecture.png"
W, H = 13.0, 8.4
fig, ax = plt.subplots(figsize=(W, H)); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
C = {"data": "#dbe9f6", "model": "#e8f1e4", "repair": "#fbe9d0", "deploy": "#ece4f4", "judge": "#fde2e1", "stat": "#f2f2f2", "kit": "#fff8d6"}


def box(x, y, w, h, title, body="", fc="#f2f2f2", fs=8.6, ts=9.4, lw=1.0, title_lines=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec="#444", lw=lw))
    ax.text(x + w / 2, y + h - 0.15, title, ha="center", va="top", fontsize=ts, weight="bold", linespacing=1.15)
    if body: ax.text(x + w / 2, y + h - 0.15 - 0.27 * title_lines - 0.05, body, ha="center", va="top", fontsize=fs, linespacing=1.3)


def arrow(x1, y1, x2, y2, text="", style="-|>", color="#333", lw=1.3, ts=7.8, dx=0, dy=0.12):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14, color=color, lw=lw, shrinkA=0, shrinkB=0))
    if text: ax.text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, text, ha="center", va="bottom", fontsize=ts, color=color)


BW, STEP, X0 = 1.86, 2.14, 0.15          # box width, column pitch, left margin -> 0.28 clear between boxes

# ---- band 1: toolkits
ax.text(X0, 8.25, "Toolkits", fontsize=12, weight="bold", va="top")
kits = [("CuratorKIT", "prompt sets, twins,\nClinicSafe-Hi, SFT corpora"), ("Transformers + PEFT", "LoRA fine-tunes,\nmerges"), ("CircuitKIT", "EAP-IG circuits,\nnecessity / sufficiency"),
        ("SafeTune", "reference for ReSta;\nsteering recipe"), ("AuditKIT", "cells, judges,\nback-translation, stats"), ("llama.cpp", "GGUF, K-quants,\ncontrol vector, server")]
for i, (t, b) in enumerate(kits): box(X0 + i * STEP, 6.95, BW, 1.05, t, b, fc=C["kit"], fs=8.0, ts=9.0)

# ---- band 2: pipeline with RQ chain
ax.text(X0, 6.72, "Pipeline and research-question chain (each stage uses the previous stage's output)", fontsize=12, weight="bold", va="top")
stages = [("RQ1  Gap", "Original model\nEN / HI / Hinglish\nclinical vs general", C["data"]),
          ("RQ2  Drift", "Medical LoRA vs\ntoken-matched control\n1,612 test prompts", C["model"]),
          ("RQ3  Cause", "Refusal circuits\nper language;\nwhat fine-tuning changed", C["model"]),
          ("RQ4  Fix", "ReSta | restricted ReSta\n| steering L24 s0.5\n(dev selects, test reports)", C["repair"]),
          ("RQ5  Last mile", "NF4; GGUF F16, Q4_K_M,\nQ3_K_M, no preamble,\nbudget-phone stack", C["deploy"]),
          ("RQ6  Protection", "Equal-size protected vs\nrandom Q3_K_M builds,\nvector attached", C["deploy"])]
for i, (t, b, c) in enumerate(stages):
    x = X0 + i * STEP; box(x, 5.0, BW, 1.45, t, b, fc=c, fs=8.0, ts=9.6)
    if i < 5: arrow(x + BW + 0.02, 5.72, x + STEP - 0.02, 5.72)
ax.text(W / 2, 4.88, "products passed along the chain:  sets + judges + baseline  →  drifted model  →  tensor map  →  deployed repair  →  stock Q3 reference  →  verdict",
        ha="center", va="top", fontsize=9.0, style="italic")

# ---- band 3: machines and hand-offs
ax.text(X0, 4.5, "Two machines, one judge", fontsize=12, weight="bold", va="top")
LX, LW, RX = 0.15, 6.0, 6.85
box(LX, 2.15, LW, 2.15, "Windows laptop lane (first author)\nRTX 4080 12 GB, Transformers",
    "data, fine-tunes, merges  •  circuits and validation\n"
    "repair sweeps; ReSta, restricted ReSta, steering cells\n"
    "NF4 cells  •  MedMCQA  •  control-vector export\n"
    "ALL JUDGING: Qwen3Guard; IndicTrans2 + WildGuard (Hindi)\n"
    "hand-label review, κ  •  bootstrap, Holm, R(s), audits",
    fc=C["judge"], fs=8.4, ts=9.4, title_lines=2)
box(RX, 2.15, LW, 2.15, "Mac lane (second author)\nApple silicon, llama.cpp (pinned build)",
    "F16 / Q4_K_M / Q3_K_M GGUF  •  EOS, template audits\n"
    "fidelity-50 gates  •  five steered deployment cells\n"
    "equal-size protected and random Q3_K_M builds\n"
    "operational checks  •  throughput, cost  •  D8 report\n"
    "sends answers (D6), receives labels (D7)",
    fc=C["deploy"], fs=8.4, ts=9.4, title_lines=2)
arrow(LX + LW + 0.02, 3.55, RX - 0.02, 3.55)      # laptop -> Mac
arrow(RX - 0.02, 2.85, LX + LW + 0.02, 2.85)      # Mac -> laptop
ax.text(LX + LW / 2, 1.72, "laptop → Mac:  D4 tensor map  •  D5b steering vector  •  D2 reference tensors  •  D7 labels", ha="center", va="center", fontsize=8.8, color="#333")
ax.text(RX + LW / 2, 1.72, "Mac → laptop:  D6 answers (ZIPs, sha256)  •  D8 results and figures", ha="center", va="center", fontsize=8.8, color="#333")
# connectors: stubs from both lane boxes to a bar, then one line down the free centre to the shared box
for xc in (LX + LW / 2, RX + LW / 2): arrow(xc, 2.15, xc, 1.98, style="-", lw=0.9, color="#777")
arrow(LX + LW / 2, 1.98, RX + LW / 2, 1.98, style="-", lw=0.9, color="#777")
arrow(W / 2, 1.98, W / 2, 0.95, style="-", lw=0.9, color="#777")
box(0.45, 0.3, 12.1, 0.62, "Shared: pre-registration (5 dated amendments, 1 withdrawn)  •  decision log  •  frozen 1,612-prompt test set  •  seed 13",
    fc=C["stat"], fs=9.0, ts=8.8)
fig.savefig(OUT, dpi=200, bbox_inches="tight"); print("written", OUT)
