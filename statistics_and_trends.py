"""
This is the template file for the statistics and trends assignment.
You will be expected to complete all the sections and
make this a fully working, documented file.
You should NOT change any function, file or variable names,
 if they are given to you here.
Make use of the functions presented in the lectures
and ensure your code is PEP-8 compliant, including docstrings.
"""


# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Ignore useless warning
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def plot_relational_plot(df):
    """
    Create a relational plot showing the evolution of the number of movies added per year.
    A line plot is used to visualize the trend over time.
    """
    
    # Check if 'date_added' column exists
    if 'date_added' in df.columns:
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')  # Convert to datetime, coerce errors
        df['year_added'] = df['date_added'].dt.year  # Extract the year from the date_added column
        yearly_counts = df['year_added'].value_counts().sort_index()  # Count the movies added each year

        # Set up the figure size
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create a line plot with blue color gradient
        sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker='o', ax=ax, color='blue')

        # Set the title and axis labels with specific font sizes and weight
        ax.set(xlabel="Year Added", ylabel="Number of Movies Added", title="Evolution of Movies Added by Year")
        ax.title.set_fontsize(20)
        ax.title.set_fontweight('bold')
        ax.xaxis.label.set_fontsize(14)
        ax.yaxis.label.set_fontsize(14)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        # Ensure tight layout and save the figure
        plt.tight_layout()
        plt.savefig('relational_plot.png')
        plt.show()
        return

  
def plot_categorical_plot(df):
    """
    Create a categorical plot (bar plot) showing the top 10 countries with the most movies.
    """
    
    if 'country' in df.columns:
        top_countries = df['country'].value_counts().head(10)  # Get top 10 countries with most movies

        # Set up the figure size
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create a bar plot with a blue color gradient
        sns.barplot(x=top_countries.values, y=top_countries.index, palette='viridis', ax=ax)

        # Set the title and axis labels with specific font sizes and weight
        ax.set(xlabel="Number of Movies", ylabel="Country", title="Top 10 Countries with the Most Movies")
        ax.title.set_fontsize(20)
        ax.title.set_fontweight('bold')
        ax.xaxis.label.set_fontsize(14)
        ax.yaxis.label.set_fontsize(14)

        # Ensure tight layout and save the figure
        plt.tight_layout()
        plt.savefig('categorical_plot.png')
        plt.show()
        return
  

def plot_statistical_plot(df):
    """
    Create a statistical plot (correlation heatmap) to visualize correlations between numerical variables.
    """
    
    numeric_df = df.select_dtypes(include=['number'])  # Select only numerical columns

    # Set up the figure size
    fig, ax = plt.subplots(figsize=(15, 6))

    # Create a heatmap with a blue color gradient for correlation
    sns.heatmap(numeric_df.corr(), annot=True, cmap='Blues', linewidths=0.5, ax=ax)

    # Set the title with specific font sizes and weight
    ax.set_title('Correlation Heatmap of Numeric Variables')
    ax.title.set_fontsize(20)
    ax.title.set_fontweight('bold')

    # Ensure tight layout and save the figure
    plt.tight_layout()
    plt.savefig('statistical_plot.png')
    plt.show()
    return


def statistical_analysis(df, col):
    """
    Perform statistical analysis on a given column:
    calculates mean, standard deviation, skewness, and excess kurtosis.
    """
    # Calculate statistical moments
    mean = df[col].mean()  # Mean of the column
    stddev = df[col].std()  # Standard deviation
    skew = df[col].skew()  # Skewness (measure of asymmetry)
    excess_kurtosis = df[col].kurtosis() - 3  # Excess kurtosis subtracts 3 to normalize

    return mean, stddev, skew, excess_kurtosis


def preprocessing(df):
    """
    Preprocess the data by cleaning missing values, converting appropriate columns,
    and providing quick insights using describe(), head(), and corr().
    """
    
    # Print preview of the first rows of the dataset
    print("Preview of the first rows of the dataset:")
    print(df.head())
    
    # Display descriptive statistics for numerical variables
    print("\nDescriptive statistics for numerical variables:")
    print(df.describe())
    
    numeric_df = df.select_dtypes(include=['number'])  # Select numerical columns for correlation
    print("\nCorrelation matrix:")
    print(numeric_df.corr())  # To avoid errors with non-numeric data

    # Drop rows with missing values in essential columns
    df.dropna(subset=['release_year', 'duration', 'country'], inplace=True)

    # Convert 'duration' to numeric by extracting minutes
    df['duration'] = df['duration'].astype(str).str.extract(r'(\d+)').astype(float)

    # Ensure 'release_year' is an integer
    df['release_year'] = df['release_year'].astype(int)

    return df


def writing(moments, col):
    """
    Print the statistical moments for a specific column and describe the distribution.
    """
    
    if moments:
        print(f'\nFor the attribute " {col} " :')
        print(f'Mean = {moments[0]:.2f}, '
              f'Standard Deviation = {moments[1]:.2f}, '
              f'Skewness = {moments[2]:.2f}, and '
              f'Excess Kurtosis = {moments[3]:.2f}.')

        # Interpretation of skewness and kurtosis
        if moments[2] > 0:
            skew = 'right-skewed'
        elif moments[2] < 0:
            skew = 'left-skewed'
        else:
            skew = 'not skewed'

        if moments[3] > 0:
            kurtosis = 'leptokurtic'
        elif moments[3] < 0:
            kurtosis = 'platykurtic'
        else:
            kurtosis = 'mesokurtic'

        print(f'The data was {skew} and {kurtosis}.')


def main():
    """
    Main function to load data, preprocess it, and generate the plots and statistical analysis.
    """
    # Load the data
    df = pd.read_csv('netflix_titles.csv')

    # Preprocess the data
    df = preprocessing(df)

    # I chose the column 'duration' for statistical analysis
    col = 'duration'

    # Generate the plots
    plot_relational_plot(df)
    plot_statistical_plot(df)
    plot_categorical_plot(df)

    # Perform statistical analysis
    moments = statistical_analysis(df, col)

    # Display the analysis
    writing(moments, col)

    return


if __name__ == '__main__':
    main()
