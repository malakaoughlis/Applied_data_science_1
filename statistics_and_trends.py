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
import pandas as pd
import seaborn as sns

# Ignore useless warning
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def plot_relational_plot(df):
    """
    Create a relational plot showing the evolution
    of the number of movies added per year.
    A line plot is used to visualize the trend over time.
    """

    # Check if 'date_added' column exists
    if 'date_added' in df.columns:
        # Convert to datetime, coerce errors
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        # Extract the year from the date_added column
        df['year_added'] = df['date_added'].dt.year
        # Count the movies added each year
        yearly_counts = df['year_added'].value_counts().sort_index()

        # Set up the figure size
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create a line plot with blue color gradient
        sns.lineplot(x=yearly_counts.index, y=yearly_counts.values,
                     marker='o', ax=ax, color='blue')

        # Set the title and axis labels with specific font sizes and weight
        ax.set(xlabel="Year Added", ylabel="Number of Movies Added",
               title="Evolution of Movies Added by Year")
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
    Create a categorical plot (bar plot) showing the
    top 10 countries with the most movies.
    """

    if 'country' in df.columns:
        # Get top 10 countries with most movies
        top_countries = df['country'].value_counts().head(10)

        # Set up the figure size
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create a bar plot with a blue color gradient
        sns.barplot(x=top_countries.values, y=top_countries.index,
                    palette='viridis', ax=ax)

        # Set the title and axis labels with specific font sizes and weight
        ax.set(xlabel="Number of Movies", ylabel="Country",
               title="Top 10 Countries with the Most Movies")
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
    Create a statistical plot (correlation heatmap)
    to visualize correlations between numerical variables.
    """

    # Select only numerical columns
    numeric_df = df.select_dtypes(include=['number'])

    # Set up the figure size
    fig, ax = plt.subplots(figsize=(15, 6))

    # Create a heatmap with a blue color gradient for correlation
    sns.heatmap(numeric_df.corr(), annot=True, cmap='Blues',
                linewidths=0.5, ax=ax)

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
    calculates mean, standard deviation, skewness,
    and excess kurtosis.
    """

    # Calculate statistical moments
    mean = df[col].mean()
    stddev = df[col].std()
    skew = df[col].skew()
    excess_kurtosis = df[col].kurtosis() - 3

    return mean, stddev, skew, excess_kurtosis


def preprocessing(df):
    """
    Preprocess the data by cleaning missing values,
    converting appropriate columns,
    and providing quick insights using describe(),
    head(), and corr().
    """

    # Print preview of the first rows of the dataset
    print("Preview of the first rows of the dataset:")
    print(df.head())

    # Display descriptive statistics for numerical variables
    print("\nDescriptive statistics for numerical variables:")
    print(df.describe())

    # Select numerical columns for correlation
    numeric_df = df.select_dtypes(include=['number'])
    print("\nCorrelation matrix:")
    # To avoid errors with non-numeric data
    print(numeric_df.corr())

    # Drop rows with missing values in essential columns
    df.dropna(subset=['release_year', 'duration', 'country'],
              inplace=True)

    # Convert 'duration' to numeric by extracting minutes
    df['duration'] = df['duration'].astype(str).\
        str.extract(r'(\d+)').astype(float)

    # Ensure 'release_year' is an integer
    df['release_year'] = df['release_year'].astype(int)

    return df


def writing(moments, col):
    """
    Print the statistical moments for a specific column
    and describe the distribution.
    """

    if moments:
        mean, stddev, skew, excess_kurtosis = moments  # Déballer les valeurs retournées

        print(f'\nFor the attribute " {col} " :')
        print(f'Mean = {mean:.2f}, '
              f'Standard Deviation = {stddev:.2f}, '
              f'Skewness = {skew:.2f}, and '
              f'Excess Kurtosis = {excess_kurtosis:.2f}.')

        # Interprétation de skewness et kurtosis
        if skew > 0:
            skewness_desc = 'right-skewed'
        elif skew < 0:
            skewness_desc = 'left-skewed'
        else:
            skewness_desc = 'not skewed'

        if excess_kurtosis > 0:
            kurtosis_desc = 'leptokurtic'
        elif excess_kurtosis < 0:
            kurtosis_desc = 'platykurtic'
        else:
            kurtosis_desc = 'mesokurtic'

        print(f'The data was {skewness_desc} and {kurtosis_desc}.')


def main():
    """
    Main function to load data, preprocess it,
    and generate the plots and statistical analysis.
    """
    df = pd.read_csv('data.csv')
    df.info()
    df = preprocessing(df)
    col = 'duration'
    plot_relational_plot(df)
    plot_statistical_plot(df)
    plot_categorical_plot(df)
    moments = statistical_analysis(df, col)
    writing(moments, col)
    return


if __name__ == '__main__':
    main()
