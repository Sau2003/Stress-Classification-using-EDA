import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# defining a function for calculation of stress level 
def calculate_stress_level(csv_file):
    df = pd.read_csv(csv_file)

    def calculate_stress(row):
        count = sum(row == "Yes")
        if count >= 4:
            return "High Stress"
        elif count == 3:
            return "Medium Stress"
        else:
            return "Low Stress"

    # Applying the calculate_stress function to each row for  creation of new 'Stress Level' column
    df['Stress Level'] = df.apply(calculate_stress, axis=1)

    return df

# Loading the CSV file and calculation of stress levels
csv_file = 'stress.csv'
result_df = calculate_stress_level(csv_file)

# Displaying the first few rows of the dataset
print(result_df.head())

# Summary statistics
print(result_df.describe())

# Check for missing values
print(result_df.isnull().sum())

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
result_df = result_df.rename(columns=short_labels)

# Map "yes" and "no" to 1 and 0 for binary variables
binary_vars = ["Academic Pressure", "Financial Stress", "Sleep Stress", "Time Management", "Interaction", "Attendance"]
for var in binary_vars:
    result_df[var] = result_df[var].map({"Yes": 1, "No": 0})

# ********************************** Univariate analysis *********************************************************


#Univariate analysis for a single variable
for var in binary_vars:
    plt.figure(figsize=(8, 6))
    sns.histplot(data=result_df, x=var, hue='Stress Level', multiple='stack', bins=10)
    plt.title(f'Distribution of {var} by Stress Level')
plt.show()

# Univariate analysis for two variables
plt.figure(figsize=(8, 6))
sns.histplot(result_df['Academic Pressure'], bins=10, color='blue', label='Academic Pressure')
sns.histplot(result_df['Time Management'], bins=10, color='green', label='Time Management')
plt.title('Distribution of Academic Pressure and Time management')
plt.legend()
plt.show()

plt.figure(figsize=(8, 6))
sns.histplot(result_df['Financial Stress'], bins=10, color='blue', label='Financial Stress')
sns.histplot(result_df['Sleep Stress'], bins=10, color='green', label='Sleep Stress')
plt.title('Distribution of financial stress vs sleep stress')
plt.legend()
plt.show()

plt.figure(figsize=(8, 6))
sns.histplot(result_df['Interaction'], bins=10, color='blue', label='Interaction')
sns.histplot(result_df['Attendance'], bins=10, color='green', label='Attendance')
plt.title('Distribution of Interaction vs Attendance')
plt.legend()
plt.show()




# ******************************** Correlation matrix for multivariate analysis *************************************

#Calculate the correlation matrix for binary variables, classified by 'Stress Level'
correlation_matrix = result_df.groupby('Stress Level')[binary_vars].corr()

# Create a heatmap of the correlation matrix for each stress level
plt.figure(figsize=(12, 7))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix Heatmap for Binary Variables by Stress Level")
plt.show()

# ************************************ Pairplot for multivariate analysis *************************************

#Creating pairplots for binary variables and classified by 'Stress Level'
plt.figure(figsize=(10, 8))
pairplot = sns.pairplot(result_df, hue='Stress Level', vars=binary_vars)

# Adjusting sizes
plt.subplots_adjust(top=0.95, hspace=0.3)
pairplot.fig.suptitle("Pairplot for Binary Variables (Yes/No) by Stress Level", size=15)


for ax in pairplot.axes.flat:
    labels_y = ax.get_yticklabels()
    ax.set_yticklabels(labels_y, rotation=90, fontsize=10)
plt.show()

# ****************************** Creating Boxplots *************************************

# Create boxplots for single variables and are classified by 'Stress Level'
for var in binary_vars:
    plt.figure(figsize=(12, 9))
    sns.boxplot(data=result_df, x=var, y='Stress Level')
    plt.title(f"Boxplot for {var} by Stress Level")
plt.show()

# Boxplot for two variables
plt.figure(figsize=(10, 6))
sns.boxplot(data=result_df, x='Academic Pressure', y='Time Management', hue='Stress Level')
plt.title('Boxplot for Academic Pressure vs. Time Management by Stress Level')
plt.show()

# Boxplot for two variables 
plt.figure(figsize=(10, 6))
sns.boxplot(data=result_df, x='Financial Stress', y='Sleep Stress', hue='Stress Level')
plt.title('Boxplot for Financial stress vs. Sleep stress by Stress Level')
plt.show()

# Boxplot for two variables 
plt.figure(figsize=(10, 6))
sns.boxplot(data=result_df, x='Attendance', y='Interaction', hue='Stress Level')
plt.title('Boxplot for Attendance vs. Interaction by Stress Level')
plt.show()

# Prediction of stress level


# Function to predict stress level
def predict_stress_level():
    print("Please answer the following questions (Yes/No):")
    answers = []
    questions = ["Do you feel academic pressure?",
                 "Do you feel financial stress?",
                 "Are you getting enough sleep (7 - 8 hrs per day)?",
                 "Do you feel stress due to poor time management?",
                 "Do you feel stress due to lack of interaction in the classroom?"]

    for question in questions:
        while True:
            response = input(f"{question} ")
            if response.lower() in ["yes", "no"]:
                answers.append(response)
                break
            else:
                print("Please enter 'Yes' or 'No' as your response.")

    # Creating a DataFrame for the user's responses
    user_data = pd.DataFrame({'User Response': answers})

    # Calculate the stress level based on the user's responses
    user_stress_level = calculate_stress_level('stress.csv')  # Pass the file path here
    predicted_stress = user_stress_level['Stress Level'].values[0]

    print(f"{name}, your predicted stress level is: {predicted_stress}")

if __name__ == "__main__":
    name = input("Please enter your name: ")
    predict_stress_level()
