import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StressLevelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stress Level Analysis")

        # Variables for file handling
        self.csv_file = ""
        self.result_df = None

        # Create a notebook (tabbed layout)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs for Predict Stress Level and Analyze CSV File
        self.create_predict_tab()
        self.create_analyze_tab()

    def create_predict_tab(self):
        predict_tab = ttk.Frame(self.notebook)
        self.notebook.add(predict_tab, text='Predict Stress Level')

        # Questionnaire Frame
        questionnaire_frame = ttk.LabelFrame(predict_tab, text="Questionnaire", padding="10")
        questionnaire_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Questions and Responses
        self.answers = []
        self.questions = ["Do you feel academic pressure?",
                          "Do you feel financial stress?",
                          "Are you not getting enough sleep (7 - 8 hrs per day)?",
                          "Do you feel stress due to poor time management?",
                          "Do you feel stress due to lack of interaction in the classroom?"]

        for i, question in enumerate(self.questions):
            ttk.Label(questionnaire_frame, text=question).grid(row=i, column=0, padx=10, pady=5)
            response_var = tk.StringVar(value="No")
            ttk.Radiobutton(questionnaire_frame, text="Yes", variable=response_var, value="Yes").grid(row=i, column=1, padx=10, pady=5)
            ttk.Radiobutton(questionnaire_frame, text="No", variable=response_var, value="No").grid(row=i, column=2, padx=10, pady=5)
            self.answers.append(response_var)

        # Button to Calculate Stress Level
        ttk.Button(predict_tab, text="Calculate Stress Level", command=self.predict_stress_level).pack(pady=20)

        # Display Area
        self.output_text_predict = tk.Text(predict_tab, width=60, height=10)
        self.output_text_predict.pack(padx=20, pady=10)

    def create_analyze_tab(self):
        analyze_tab = ttk.Frame(self.notebook)
        self.notebook.add(analyze_tab, text='Analyze CSV File')

        # File Loading Section
        frame = ttk.LabelFrame(analyze_tab, text="File Loading", padding="10")
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # File Path Label
        ttk.Label(frame, text="CSV File:").grid(row=0, column=0, sticky="w")

        # Entry to show selected file path
        self.file_path_entry = ttk.Entry(frame, width=50, state="readonly")
        self.file_path_entry.grid(row=0, column=1, padx=5, pady=5)

        # Browse Button
        ttk.Button(frame, text="Browse", command=self.load_csv_file).grid(row=0, column=2, padx=5, pady=5)

        # Calculate Stress Levels Button
        ttk.Button(frame, text="Calculate Stress Levels", command=self.calculate_and_visualize).grid(row=1, column=0, columnspan=3, pady=10)

        # Canvas for Plot Display
        self.plot_canvas = tk.Canvas(analyze_tab, width=800, height=600)
        self.plot_canvas.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    def load_csv_file(self):
        self.csv_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.file_path_entry.config(state="normal")
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, self.csv_file)
        self.file_path_entry.config(state="readonly")

    def calculate_stress_level(self, user_data):
        def calculate_stress(row):
            count = sum(row == "Yes")
            if count >= 4:
                return "High Stress"
            elif count == 3:
                return "Medium Stress"
            else:
                return "Low Stress"

        stress_level = calculate_stress(user_data.values.flatten())
        return stress_level

    def predict_stress_level(self):
        answers = [var.get() for var in self.answers]
        user_data = pd.DataFrame({'User Response': answers})
        stress_level = self.calculate_stress_level(user_data)
        self.output_text_predict.delete(1.0, tk.END)
        self.output_text_predict.insert(tk.END, f"Your predicted stress level is: {stress_level}")

    def calculate_and_visualize(self):
        try:
            self.result_df = pd.read_csv(self.csv_file)
            self.result_df = self.calculate_stress_level_csv(self.result_df)

            # Create a dictionary to map long variable names to shorter labels
            short_labels = {
                "Do you feel academic pressure?": "Academic Pressure",
                "Do you feel financial  stress?": "Financial Stress",
                "Are you getting enough sleep(7 - 8hrs per day)?": "Sleep Stress",
                "Do you feel stress due to poor Time Management?": "Time Management",
                "Do you feel stress due to lack of interaction in classroom?": "Interaction",
                "Do you feel stress due to the tight deadlines of college assignments and strict attendance?": "Attendance"
            }

            # Rename columns in the DataFrame with shorter labels
            self.result_df = self.result_df.rename(columns=short_labels)

            # Map "yes" and "no" to 1 and 0 for binary variables
            binary_vars = ["Academic Pressure", "Financial Stress", "Sleep Stress", "Time Management", "Interaction", "Attendance"]
            for var in binary_vars:
                self.result_df[var] = self.result_df[var].map({"Yes": 1, "No": 0})

            # Display correlation matrix
            self.display_correlation_matrix()

        except Exception as e:
            messagebox.showerror("Error", f"Error in calculating stress levels: {e}")

    def calculate_stress_level_csv(self, df):
        def calculate_stress(row):
            count = sum(row == "Yes")
            if count >= 4:
                return "High Stress"
            elif count == 3:
                return "Medium Stress"
            else:
                return "Low Stress"

        df['Stress Level'] = df.apply(calculate_stress, axis=1)
        return df

    def display_correlation_matrix(self):
        # Calculate the correlation matrix for binary variables, classified by 'Stress Level'
        correlation_matrix = self.result_df.groupby('Stress Level')[["Academic Pressure", "Financial Stress", "Sleep Stress", "Time Management", "Interaction", "Attendance"]].corr()

        # Display the correlation matrix as a heatmap
        self.plot_canvas.delete("all")
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Correlation Matrix Heatmap for Binary Variables by Stress Level")
        plt.tight_layout()

        # Embedding matplotlib plot into Tkinter canvas
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = StressLevelApp(root)
    root.mainloop()
