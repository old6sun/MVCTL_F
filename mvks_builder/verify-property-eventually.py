import numpy as np
import re
import matplotlib.pyplot as plt

from maxmin import max_min_composition_numpy

def calculate_P_plus(P):

    P = np.array(P)
    N = P.shape[0]
    P_k = np.copy(P)
    P_plus = np.copy(P)

    for _ in range(1, N):
        P_k = max_min_composition_numpy(P_k, P)
        P_plus = np.maximum(P_plus, P_k)
    return P_plus

def calculate_P_star(P_plus):

    N = P_plus.shape[0]
    P_0 = np.eye(N)
    return np.maximum(P_0, P_plus)

def calculate_r_P(P_plus):

    P_plus = np.array(P_plus)
    diag_elements = np.diagonal(P_plus)
    D = diag_elements.reshape(-1, 1)
    return max_min_composition_numpy(P_plus, D)

def calculate_diamond_phi(P_star, D_phi, r_P):

    step1 = max_min_composition_numpy(D_phi, r_P)
    diamond_phi = max_min_composition_numpy(P_star, step1)
    return diamond_phi

def extract_GPKS_matrices(p_matrix, all_states):

    N = len(all_states)
    P_matrix_list = []
    V_phi = np.zeros(N)
    ap8_pattern = re.compile(r'AP8=([^,)]+)')

    for i, si in enumerate(all_states):
        row_vals = []
        for sj in all_states:
            prob = p_matrix.get(si, {}).get(sj, 0.0)
            row_vals.append(prob)

        P_matrix_list.append(row_vals)

        match = ap8_pattern.search(si)
        if match:
            ap8_val_str = match.group(1).strip()
            try:
                original_val = float(ap8_val_str)

                if "Output Layer" in si:
                    V_phi[i] = 1.0 - original_val
                else:
                    V_phi[i] = original_val

            except ValueError:
                V_phi[i] = 0.0

    P_matrix = np.array(P_matrix_list)
    D_phi = np.zeros((N, N))
    np.fill_diagonal(D_phi, V_phi)

    return P_matrix, D_phi

if __name__ == '__main__':
    from mvks_builder import build_mvks_from_json

    file_path = "test.json"
    print("⏳ Building mvKS state space and transition matrix...")
    _, p_matrix_dict, all_states = build_mvks_from_json(file_path)

    N = len(all_states)
    print(f"✅ Build complete. Total states: {N}\n")

    print("⏳ Parsing and extracting P matrix and D_Φ matrix...")
    P_matrix, D_phi = extract_GPKS_matrices(p_matrix_dict, all_states)

    print("⏳ Calculating transitive closure P^+ and equivalent matrix P^* ...")
    P_plus = calculate_P_plus(P_matrix)
    P_star = calculate_P_star(P_plus)

    D_vector = np.ones((N, 1))
    r_P = calculate_r_P(P_plus)

    print("⏳ Calculating ♢Φ = P^* ∘ D_Φ ∘ r_P ...")
    diamond_phi = calculate_diamond_phi(P_star, D_phi, r_P)

    print("\n" + "=" * 50)
    print("🎯 Final result: Probability measure of formula ♢Φ (Eventually reaching safe rejection state)")
    print("=" * 50)

    plot_states = []
    plot_measures = []

    for i in range(N):
        state_id = f"S{i}"
        measure = diamond_phi[i][0]
        ap8_val = D_phi[i][i]

        plot_states.append(state_id)
        plot_measures.append(measure)

        print(f"[{state_id:>3}] {all_states[i]}")
        print(f"      -> Own AP8 Value: {ap8_val:>4.2f}")
        print(f"      -> ♢Φ Satisfaction: {measure:>4.2f}\n")

    print("⏳ Generating result distribution line chart...")

    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(14, 6))

    plt.plot(plot_states, plot_measures, marker='o', color='steelblue', linestyle='-', linewidth=2, markersize=5)

    plt.xticks(rotation=90, fontsize=8)

    plt.title("Probability measure distribution of ♢Φ (Eventually safe rejection) across states", fontsize=14, pad=15)
    plt.xlabel("States", fontsize=12)
    plt.ylabel("Measure", fontsize=12)

    plt.ylim(0, 1.05)

    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.grid(axis='x', linestyle=':', alpha=0.4)

    plt.tight_layout()

    plt.savefig("diamond_phi_results_line.png", dpi=300)
    print("✅ Chart saved as diamond_phi_results_line.png")
    plt.show()

    print("\n⏳ Exporting matrices to CSV...")
    np.savetxt("P_matrix.csv", P_matrix, delimiter=",", fmt="%.4f")
    np.savetxt("P_star_matrix.csv", P_star, delimiter=",", fmt="%.4f")
    np.savetxt("D_phi_matrix.csv", D_phi, delimiter=",", fmt="%.4f")
    np.savetxt("r_P_vector.csv", r_P, delimiter=",", fmt="%.4f")
    print("✅ All CSV files exported!")