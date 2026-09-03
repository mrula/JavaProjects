'''
Random walk script

'''

import matplotlib.pyplot as plt
import io
import base64
import json
import numpy as np
import sys

def run_random_walk(BM):

    #%% Follow only a few markers

    # Number of markers (particles)
    n = 1

    ## Draw 'nsteps' random step sizes from a given distribution (either Gaussian or Lévy alpha-stable)
    nsteps = 100

    # Initial location of markers. n rows (# of markers)
    x = np.zeros((n, nsteps + 1))
    y = np.zeros((n, nsteps + 1))

    # ===========================================================================================
    
    if BM:
    
        #%% Random walk from normal Gaussian steps

        for i in range(nsteps):
            xstep = np.random.normal(0, 1, size=n)
            ystep = np.random.normal(0, 1, size=n)

            x[:, i + 1] = x[:, i] + xstep
            y[:, i + 1] = y[:, i] + ystep

        # Make figure
        fig, ax = plt.subplots()
        fig.patch.set_facecolor("#1e293b")
        ax.plot(x[0,:].T, y[0,:].T, linewidth=1.5, color="#d1d1d1")
        ax.set_facecolor("#1e293b")
        ax.set_title('Random walk')
        ax.set_xlabel('x', size=12, color="#d1d1d1")
        ax.set_ylabel('y', size=12, color="#d1d1d1")
        ax.set_aspect('equal')
        ax.set_xlim([-20, 20])
        ax.set_ylim([-20, 20])
        ax.tick_params(
            axis="both",
            colors="#d1d1d1"
        )
        for spine in ax.spines.values():
            spine.set_color("#d1d1d1")

        # Convert figure to PNG in memory
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", bbox_inches="tight")
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        plt.close(fig)


    # ===========================================================================================
    
    else:
    
        #%% Lévy flight from Lévy alpha-stable steps

        from scipy.stats import levy_stable

        # Lévy alpha-stable distribution parameters
        alpha = 1.5
        beta  = 0.0

        for i in range(nsteps):
            # Draw steps in x direction
            # xsteps = np.minimum(np.maximum(levy_stable.rvs(alpha, beta, size=(n,nsteps)), -10*np.ones((n,nsteps))), 10*np.ones((n,nsteps)))
            rstep = levy_stable.rvs(alpha, beta, size=n)

            # Draw steps in y direction
            # ysteps = np.minimum(np.maximum(levy_stable.rvs(alpha, beta, size=(n,nsteps)), -10*np.ones((n,nsteps))), 10*np.ones((n,nsteps)))
            phistep = np.random.uniform(low=0.0, high=2*np.pi, size=n)

            # Convert to Cartesian coordinates
            xstep = rstep*np.cos(phistep)
            ystep = rstep*np.sin(phistep)
            
            # Take step
            x[:, i + 1] = x[:, i] + xstep
            y[:, i + 1] = y[:, i] + ystep

        fig, ax = plt.subplots()
        fig.patch.set_facecolor("#1e293b")
        ax.plot(x[0,:].T, y[0,:].T, linewidth=1.5, color="#d1d1d1")
        ax.set_facecolor("#1e293b")
        ax.set_title('Lévy flight')
        ax.set_xlabel('x', size=12, color="#d1d1d1")
        ax.set_ylabel('y', size=12, color="#d1d1d1")
        ax.set_aspect('equal')
        ax.set_xlim([-20, 20])
        ax.set_ylim([-20, 20])
        ax.tick_params(
            axis="both",
            colors="#d1d1d1"
        )
        for spine in ax.spines.values():
            spine.set_color("#d1d1d1")


        # Convert figure to PNG in memory
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", bbox_inches="tight")
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        plt.close(fig)

        # ===========================================================================================

    # Return dictionary
    text = "Holy moly!"
    return {
        "result": text,
        "plot": image_base64,
        # JSON cannot serialise numpy arrays, so I make them lists instead
        "x": x[0,:].tolist(), # To make interactive figure in html as well
        "y": y[0,:].tolist() # To make interactive figure in html as well
    }

if __name__ == "__main__":
    # Read input
    BM = sys.argv[1].lower() == "true"
    # Dump output as JSON and pass that to the browser
    print(json.dumps(run_random_walk(BM)))