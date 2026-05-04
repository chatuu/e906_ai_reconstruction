import os
import numpy as np
import uproot
import matplotlib.pyplot as plt

def apply_cuts(tree, cut=4.2):
    """Applies standard physics cuts to the given TTree arrays in numpy."""
    # Read all branches into a dictionary of numpy arrays
    events = tree.arrays(library="np")
    
    class EventNamespace:
        def __init__(self, data):
            self.__dict__.update(data)
    
    e = EventNamespace(events)

    bo = np.where(e.runID >= 11000, 1.6, 0.4)

    dimuon_cut = (
        (np.abs(e.dx) < 0.25) & (np.abs(e.dy - bo) < 0.22) &
        (e.dz < -5.) & (e.dz > -280.) & (np.abs(e.dpx) < 1.8) & (np.abs(e.dpy) < 2.0) &
        (e.dpx * e.dpx + e.dpy * e.dpy < 5.) & (e.dpz < 116.) & (e.dpz > 38.) &
        (e.mass > cut) & (e.mass < 8.8) &
        (e.dx * e.dx + (e.dy - bo) * (e.dy - bo) < 0.06) &
        (e.xF < 0.95) & (e.xF > -0.1) & (e.xT > 0.05) & (e.xT <= 0.58) &
        (np.abs(e.costh) < 0.5) & (np.abs(e.trackSeparation) < 270.) &
        (e.chisq_dimuon < 18)
    )

    track1_cut = (
        (e.chisq1_target < 15.) & (e.pz1_st1 > 9.) & (e.pz1_st1 < 75.) & (e.nHits1 > 13) &
        (e.x1_t * e.x1_t + (e.y1_t - bo) * (e.y1_t - bo) < 320.) &
        (e.x1_d * e.x1_d + (e.y1_d - bo) * (e.y1_d - bo) < 1100.) &
        (e.x1_d * e.x1_d + (e.y1_d - bo) * (e.y1_d - bo) > 16.) &
        (e.chisq1_target < 1.5 * e.chisq1_upstream) & (e.chisq1_target < 1.5 * e.chisq1_dump) &
        (e.z1_v < -5.) & (e.z1_v > -320.) & (e.chisq1 / (e.nHits1 - 5) < 12) &
        ((e.y1_st1) / (e.y1_st3) < 1.) & (np.abs(np.abs(e.px1_st1 - e.px1_st3) - 0.416) < 0.008) &
        (np.abs(e.py1_st1 - e.py1_st3) < 0.008) & (np.abs(e.pz1_st1 - e.pz1_st3) < 0.08) &
        ((e.y1_st1) * (e.y1_st3) > 0.) & (np.abs(e.py1_st1) > 0.02)
    )

    track2_cut = (
        (e.chisq2_target < 15.) & (e.pz2_st1 > 9.) & (e.pz2_st1 < 75.) & (e.nHits2 > 13) &
        (e.x2_t * e.x2_t + (e.y2_t - bo) * (e.y2_t - bo) < 320.) &
        (e.x2_d * e.x2_d + (e.y2_d - bo) * (e.y2_d - bo) < 1100.) &
        (e.x2_d * e.x2_d + (e.y2_d - bo) * (e.y2_d - bo) > 16.) &
        (e.chisq2_target < 1.5 * e.chisq2_upstream) & (e.chisq2_target < 1.5 * e.chisq2_dump) &
        (e.z2_v < -5.) & (e.z2_v > -320.) & (e.chisq2 / (e.nHits2 - 5) < 12) &
        ((e.y2_st1) / (e.y2_st3) < 1.) & (np.abs(np.abs(e.px2_st1 - e.px2_st3) - 0.416) < 0.008) &
        (np.abs(e.py2_st1 - e.py2_st3) < 0.008) & (np.abs(e.pz2_st1 - e.pz2_st3) < 0.08) &
        ((e.y2_st1) * (e.y2_st3) > 0.) & (np.abs(e.py2_st1) > 0.02)
    )

    tracks_cut = (
        (np.abs(e.chisq1_target + e.chisq2_target - e.chisq_dimuon) < 2.) &
        ((e.y1_st3) * (e.y2_st3) < 0.) & (e.nHits1 + e.nHits2 > 29) &
        (e.nHits1St1 + e.nHits2St1 > 8) & (np.abs(e.x1_st1 + e.x2_st1) < 42)
    )

    occ_cut = (
        (e.D1 < 400) & (e.D2 < 400) & (e.D3 < 400) & (e.D1 + e.D2 + e.D3 < 1000)
    )

    total_cut_mask = (track1_cut & track2_cut & tracks_cut & dimuon_cut & occ_cut)
    
    return e, total_cut_mask

def plot_and_save(data, filename, xlabel_text, color):
    """Helper function to create and save individual ROOT-style plots."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Draw histogram
    ax.hist(data, bins=100, color=color, edgecolor='black', alpha=0.7)
    
    # 2. ROOT Equivalent of SetPadTickx(1) and SetPadTicky(1)
    # direction='in' makes ticks point inward
    # top=True, right=True draws ticks on the top and right axes
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True, length=6)
    
    # 3 & 4. Set centered labels with LaTeX formatting for the subscript
    # loc='center' acts like ROOT's CenterTitle for axes
    ax.set_xlabel(xlabel_text, loc='center', fontsize=14)
    ax.set_ylabel("Counts", loc='center', fontsize=14)
    
    plt.tight_layout()
    
    # 1. Save as PDF
    plt.savefig(filename, format='pdf', dpi=300)
    print(f"Plot saved successfully as {filename}")
    
    # Close the figure to free up memory
    plt.close(fig)

def main():
    file_path = os.path.expanduser("~/github/e906_ai_reconstruction/root_files/roadset57_70_R008_2111v42_tmp_noPhys.root")
    tree_name = "Tree" 
    
    print(f"Opening {file_path}...")
    
    with uproot.open(file_path) as f:
        if tree_name not in f:
            print(f"Error: TTree '{tree_name}' not found. Available keys: {f.keys()}")
            return
            
        tree = f[tree_name]
        
        print("Applying cuts (this may take a moment depending on the tree size)...")
        event_data, mask = apply_cuts(tree)
        
        # Filter the arrays based on the boolean mask
        dpx_filtered = event_data.dpx[mask]
        dpy_filtered = event_data.dpy[mask]
        dpz_filtered = event_data.dpz[mask]
        
        print(f"Cuts applied. Total events: {len(mask)} | Events passing cuts: {np.sum(mask)}")
        print("Generating and saving PDF plots...")
        
        # Generate the three separate PDF plots using the helper function
        # The 'r' before the string ensures the LaTeX syntax is interpreted correctly
        plot_and_save(dpx_filtered, "dpx_kinematics.pdf", r"Dimuon $P_{x}$ (GeV)", 'royalblue')
        plot_and_save(dpy_filtered, "dpy_kinematics.pdf", r"Dimuon $P_{y}$ (GeV)", 'crimson')
        plot_and_save(dpz_filtered, "dpz_kinematics.pdf", r"Dimuon $P_{z}$ (GeV)", 'forestgreen')

if __name__ == "__main__":
    main()