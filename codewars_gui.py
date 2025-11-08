import tkinter as tk
import webbrowser
from utils.assessments import ASSESSMENTS, check_prediction_text

SIMULATIONS = {
    "Physics — Projectile Motion": "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_en.html",
    "Math — Probability": "https://phet.colorado.edu/sims/html/probability/latest/probability_en.html",
    "Biology — Diffusion & Osmosis": "https://phet.colorado.edu/sims/html/diffusion-and-osmosis/latest/diffusion-and-osmosis_en.html"
}

class CodewarsLikeGUI:
    def __init__(self, root):
        self.root = root
        root.title("Concept Visualization — Codewars-style Interface")
        root.geometry("1000x650")
        root.configure(bg="#1e1e1e")

        # Header
        header = tk.Frame(root, bg="#111111", height=70)
        header.pack(side="top", fill="x")
        title = tk.Label(header, text="Interactive Simulations", bg="#111111", fg="#f7f7f7",
                         font=("Segoe UI", 20, "bold"), padx=10, pady=10)
        title.pack(side="left")

        # Main area
        main = tk.Frame(root, bg="#1e1e1e")
        main.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(main, bg="#222222", width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Categories", bg="#222222", fg="#dddddd",
                 font=("Segoe UI", 12, "bold")).pack(pady=(12,6))

        for name in SIMULATIONS.keys():
            b = tk.Button(sidebar, text=name, anchor="w", justify="left",
                          bg="#2b2b2b", fg="#ffffff", bd=0, padx=12, pady=10,
                          activebackground="#3a3a3a", font=("Segoe UI", 11),
                          command=lambda n=name: self.select_simulation(n))
            b.pack(fill="x", padx=10, pady=6)

        # Central panel
        self.central = tk.Frame(main, bg="#1e1e1e")
        self.central.pack(side="right", fill="both", expand=True)

        self.sim_title = tk.Label(self.central, text="Welcome", bg="#1e1e1e",
                                  fg="#ffffff", font=("Segoe UI", 18, "bold"))
        self.sim_title.pack(pady=(24,8))

        self.sim_desc = tk.Label(self.central, text="Select a simulation from the left.\nOfficial PhET simulations will open in your browser.",
                                 bg="#1e1e1e", fg="#cccccc", font=("Segoe UI", 12), justify="left", wraplength=620)
        self.sim_desc.pack(pady=(6,16), padx=20)

        # Launch button
        self.launch_btn = tk.Button(self.central, text="Launch Simulation", bg="#4a90e2", fg="white",
                                    font=("Segoe UI", 12, "bold"), padx=10, pady=8, command=self.launch_current)
        self.launch_btn.pack(pady=(6,12))

        # Prediction / Assessment area
        ass_frame = tk.Frame(self.central, bg="#1e1e1e")
        ass_frame.pack(pady=(12,6), padx=20, fill="x")
        tk.Label(ass_frame, text="Prediction (enter a number):", bg="#1e1e1e", fg="#dddddd").grid(row=0, column=0, sticky="w")
        self.pred_entry = tk.Entry(ass_frame, width=20)
        self.pred_entry.grid(row=1, column=0, sticky="w", pady=6)
        self.check_btn = tk.Button(ass_frame, text="Check Prediction", command=self.check_prediction, bg="#3a3a3a", fg="white")
        self.check_btn.grid(row=1, column=1, padx=10)
        self.result_label = tk.Label(ass_frame, text="", bg="#1e1e1e", fg="#aaffaa")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=8, sticky="w")

        # Footer / explanation steps
        self.step_frame = tk.Frame(self.central, bg="#161616")
        self.step_frame.pack(side="bottom", fill="x", pady=12)
        self.step_label = tk.Label(self.step_frame, text="", bg="#161616", fg="#cccccc", wraplength=900, justify="left")
        self.step_label.pack(padx=12, pady=8)

        # initialize
        self.current_sim = None
        self.select_simulation(list(SIMULATIONS.keys())[0])

    def select_simulation(self, name):
        self.current_sim = name
        url = SIMULATIONS[name]
        self.sim_title.config(text=name)
        desc = f"Official PhET simulation will open in your browser when you click 'Launch Simulation'.\n\nURL: {url}"
        self.sim_desc.config(text=desc)
        # show assessment hint if available
        hint = ASSESSMENTS.get(name, {}).get("hint", "Try interacting with the simulation and make a prediction.")
        self.step_label.config(text="Hint: " + hint)
        self.result_label.config(text="")
        self.pred_entry.delete(0, tk.END)

    def launch_current(self):
        if not self.current_sim:
            return
        webbrowser.open(SIMULATIONS[self.current_sim])

    def check_prediction(self):
        txt = self.pred_entry.get().strip()
        if txt == "":
            self.result_label.config(text="Enter a number to check.")
            return
        ok, message = check_prediction_text(self.current_sim, txt)
        self.result_label.config(text=message, fg="#aaffaa" if ok else "#ff7777")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodewarsLikeGUI(root)
    root.mainloop()
