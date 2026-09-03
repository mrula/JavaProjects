// Random walk function to be imported by the appropriate html page

function plotRandomWalk(x, y, BM = true) {

    // Optional argument 'BM' denotes whether it's Brownian motion or Levy flights
    // Create the Plotly graph trace object
    const trace = {
        x: x,
        y: y,
        mode: "lines",
        type: "scatter",
        line: {
            color: "#d1d1d1",
            width: 1.5
        }
    };

    // Layout object of figure
    const layout = {
        paper_bgcolor: "#1e293b",
        plot_bgcolor: "#1e293b",

        font: {
            color: "#d1d1d1"
        },

        margin: {
            l: 50, // Leave some margin for the y-axis to be visible
            r: 30,
            t: 30,
            b: 50  // Leave some margin for the x-axis to be visible
        },

        xaxis: {
            title: {
                text: "x",
                font: {
                    color: "#d1d1d1",
                    size: 12
                },
                standoff: 8 /* distance from axis to label */
            },
            range: [-20, 20],
            tickfont: {
                color: "#d1d1d1"
            },
            gridcolor: "#475569",
            linecolor: "#d1d1d1",
            linewidth: 1,
            showline: true
        },

        yaxis: {
            title: {
                text: "y",
                font: {
                    color: "#d1d1d1",
                    size: 12
                },
                standoff: 8 /* distance from axis to label */
            },
            range: [-20, 20],
            scaleanchor: "x",
            scaleratio: 1,    /* like matplotlib set_aspect('equal') */
            tickfont: {
                color: "#d1d1d1"
            },
            gridcolor: "#475569",
            linecolor: "#d1d1d1",
            linewidth: 1,
            showline: true
        }
    }

    // Actually plot the interactive figure
    if (BM) {
        Plotly.newPlot("BMplotInter", [trace], layout);
    } else {
        Plotly.newPlot("LFplotInter", [trace], layout);
    }
}

// An asynchrounous function allows the webpage to not freeze while this function is ongoing
async function runRW(BM) {
    // fetch() makes a request to the python server which takes some time
    // await tells the program to wait for the operation to finish before continuing this function
    // This allows the user to still use the webpage while the python script is running
    const response = await fetch("/runRW", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ BM: BM })
    });

    const result = await response.json();

    console.log(result);

    /* THIS IS OUTDATED, AS I NOW USE THE INTERACTIVE FIGURE
    // To make the result actually appear in the paragraph <p>
    document.getElementById("RWresult").textContent = result.result;

    // To get the plot output from the random walk written in base64. The browser will convert it to an image
    const plot = document.getElementById("RWplot");
    plot.src = "data:image/png;base64," + result.plot;
    plot.style.display = "block"; // This styling should be put in the .css file.
    
    console.log(result.result);
    console.log(result.plot);
    */
    
    // To get the plot output from the random walk as data and then plotted using java functions, so it is more interactive
    // Data from python

    // Random walk data
    const x = result.x;
    const y = result.y;

    // Call plotting function
    plotRandomWalk(x, y, BM);
}