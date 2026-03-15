# -*- coding: utf-8 -*-
"""
plot_delta_tq.py

Research-oriented analysis script for Δt(Q) evaluation of lithium-ion
battery charging experiments based on NGU201 CSV exports.

Main functions
--------------
1. Read NGU201 CSV files
2. Support manual file selection or automatic CSV scanning
3. Automatically identify the DC-only reference condition
4. Compute Δt(Q) relative to the reference condition
5. Generate a multi-condition Δt(Q) comparison plot
6. Generate an AΔt bar chart up to SOC = 80%

Methodological principles
-------------------------
- Δt(Q) is defined based on Q(t)
- SOC is used only for defining the state interval
- AΔt is the integral of Δt(Q) up to SOC = 80 %

Author
------
Jiaxing Lu
"""

# ==============================
# 读取 NGU201 CSV
# ==============================

import os
import re
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ==============================
# 用户输入区
# ==============================

manual_files = []

Q_NET_AH = 3.275
SOC_TARGET = 0.80
Q_TARGET = Q_NET_AH * SOC_TARGET

CURRENT_THRESHOLD_A = 0.05
N_INTERP = 2000

OUTPUT_DELTA_T = os.path.join("results", "figures", "delta_t_Q_multi.png")
OUTPUT_A_BAR = os.path.join("results", "figures", "A_delta_t_bar_SOC80.png")


# ==============================
# 查找表头
# ==============================

def find_header(file_path, max_lines=1000):

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for i in range(max_lines):
            line = f.readline()
            if not line:
                break
            if "Timestamp" in line and "U1" in line and "I1" in line:
                return i

    raise RuntimeError(f"Header not found in CSV: {file_path}")


# ==============================
# 时间解析
# ==============================

def parse_timestamp(series):

    nums = pd.to_numeric(series, errors="coerce")

    if nums.notna().sum() > 0:
        t = nums.to_numpy(dtype=float)

        if np.nanmedian(t) > 1e4:
            t = t / 1000.0

        return t

    def parse_one(s):

        s = str(s).strip()

        m = re.match(r"^(\d{1,3}):(\d{2})(\.\d+)?$", s)
        if m:
            mm = int(m.group(1))
            ss = int(m.group(2))
            frac = float(m.group(3)) if m.group(3) else 0.0
            return mm * 60 + ss + frac

        m = re.match(r"^(\d{1,2}):(\d{2}):(\d{2})(\.\d+)?$", s)
        if m:
            hh = int(m.group(1))
            mm = int(m.group(2))
            ss = int(m.group(3))
            frac = float(m.group(4)) if m.group(4) else 0.0
            return hh * 3600 + mm * 60 + ss + frac

        return np.nan

    return series.map(parse_one).to_numpy(dtype=float)


def unwrap_time(t):

    t = np.asarray(t, dtype=float).copy()

    offset = 0.0
    prev = t[0]

    for i in range(1, len(t)):
        if t[i] + offset < prev - 300:
            offset += 3600

        t[i] += offset
        prev = t[i]

    return t


# ==============================
# CSV读取
# ==============================

def read_ngu_csv(file_path):

    header_row = find_header(file_path)

    df = pd.read_csv(file_path, skiprows=header_row)
    df.columns = [str(c).strip() for c in df.columns]

    ts_col = next(c for c in df.columns if "timestamp" in c.lower())
    u_col = next(c for c in df.columns if c.lower().startswith("u1"))
    i_col = next(c for c in df.columns if c.lower().startswith("i1"))

    t_s = parse_timestamp(df[ts_col])
    t_s = unwrap_time(t_s)

    U = pd.to_numeric(df[u_col], errors="coerce").to_numpy(dtype=float)
    I = pd.to_numeric(df[i_col], errors="coerce").to_numpy(dtype=float)

    mask = np.isfinite(t_s) & np.isfinite(U) & np.isfinite(I)

    t_s, U, I = t_s[mask], U[mask], I[mask]

    order = np.argsort(t_s)

    t_s, U, I = t_s[order], U[order], I[order]

    idx = np.where(np.abs(I) >= CURRENT_THRESHOLD_A)[0]

    start = idx[0]

    t_s, U, I = t_s[start:], U[start:], I[start:]

    t_s = t_s - t_s[0]
    t_min = t_s / 60.0

    dt = np.diff(t_s)

    Q_Ah = np.concatenate([
        [0.0],
        np.cumsum(0.5 * (I[1:] + I[:-1]) * dt)
    ]) / 3600.0

    Q_Ah = np.maximum.accumulate(Q_Ah)

    return {
        "file": file_path,
        "name": os.path.basename(file_path),
        "t_s": t_s,
        "t_min": t_min,
        "U": U,
        "I": I,
        "Q_Ah": Q_Ah
    }


# ==============================
# 文件收集
# ==============================

def collect_csv_files():

    script_dir = os.path.dirname(os.path.abspath(__file__))

    if manual_files:
        files = [os.path.join(script_dir, f) for f in manual_files]
    else:
        files = sorted(glob.glob(os.path.join(script_dir, "*.csv")))

    return files


# ==============================
# 参考工况选择
# ==============================

def choose_reference_key(data_dict):

    for key in data_dict.keys():

        name = os.path.basename(key).lower()

        if "dc" in name:
            return key

    return list(data_dict.keys())[0]


# ==============================
# Δt(Q)
# ==============================

def compute_delta_t_q(reference_data, target_data):

    q_ref = reference_data["Q_Ah"]
    t_ref = reference_data["t_min"]

    q_tar = target_data["Q_Ah"]
    t_tar = target_data["t_min"]

    q_max = min(q_ref[-1], q_tar[-1])

    q_common = np.linspace(0.0, q_max, N_INTERP)

    t_ref_interp = np.interp(q_common, q_ref, t_ref)
    t_tar_interp = np.interp(q_common, q_tar, t_tar)

    delta_t = t_ref_interp - t_tar_interp

    return q_common, delta_t


# ==============================
# AΔt
# ==============================

def compute_A_delta_t(q_common, delta_t):

    mask = q_common <= Q_TARGET

    q_cut = q_common[mask]
    dt_cut = delta_t[mask]

    if len(q_cut) < 2:
        return np.nan

    return np.trapz(dt_cut, q_cut)


# ==============================
# Δt(Q)图
# ==============================

def plot_delta_t(results):

    os.makedirs("results/figures", exist_ok=True)

    plt.figure(figsize=(8,5))

    for item in results:

        plt.plot(
            item["Q_common"],
            item["delta_t"],
            linewidth=2,
            label=f"{item['name']} | AΔt={item['A_dt']:.3f}"
        )

    plt.axvline(Q_TARGET, linestyle="--", color="black")

    plt.xlabel("Q (Ah)")
    plt.ylabel("Δt(Q) (min)")
    plt.title("Δt(Q) Charging Comparison")
    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.savefig(OUTPUT_DELTA_T, dpi=300)

    plt.show()


# ==============================
# 主程序
# ==============================

def main():

    csv_files = collect_csv_files()

    data = {}

    for f in csv_files:

        d = read_ngu_csv(f)

        data[f] = d

    ref_key = choose_reference_key(data)

    ref_data = data[ref_key]

    results = []

    for key, tar_data in data.items():

        if key == ref_key:
            continue

        q_common, delta_t = compute_delta_t_q(ref_data, tar_data)

        A_dt = compute_A_delta_t(q_common, delta_t)

        results.append({
            "name": tar_data["name"],
            "Q_common": q_common,
            "delta_t": delta_t,
            "A_dt": A_dt
        })

    plot_delta_t(results)


if __name__ == "__main__":
    main()
