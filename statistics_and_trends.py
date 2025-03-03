import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def plot_relational_plot(df):
    if 'date_added' in df.columns:
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        yearly_counts = df['date_added'].dt.year.value_counts().sort_index()
        sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker='o', color='blue')
        plt.title("Evolution of Movies Added by Year", fontsize=20, fontweight='bold')
        plt.xlabel("Year Added", fontsize=14)
        plt.ylabel("Number of Movies Added", fontsize=14)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('relational_plot.png')
        plt.show()

def plot_categorical_plot(df):
    if 'country' in df.columns:
        top_countries = df['country'].value_counts().head(10)
        sns.barplot(x=top_countries.values, y=top_countries.index, palette='viridis')
        plt.title("Top 10 Countries with the Most Movies", fontsize=20, fontweight='bold')
        plt.xlabel("Number of Movies", fontsize=14)
        plt.ylabel("Country", fontsize=14)
        plt.tight_layout()
        plt.savefig('categorical_plot.png')
        plt.show()

def plot_statistical_plot(df):
    numeric_df = df.select_dtypes(include=['number'])
    sns.heatmap(numeric_df.corr(), annot=True, cmap='Blues', linewidths=0.5)
    plt.title('Correlation Heatmap of Numeric Variables', fontsize=20, fontweight='bold')
    plt.tight_layout()
    plt.savefig('statistical_plot.png')
    plt.show()

def statistical_analysis(df, col):
    return df[col].mean(), df[col].std(), df[col].skew(), df[col].kurtosis() - 3

def preprocessing(df):
    print("Preview of dataset:", df.head(), "\nDescriptive statistics:", df.describe(), "\nCorrelation matrix:", df.corr(), sep='\n')
    df.dropna(subset=['release_year', 'duration', 'country'], inplace=True)
    df['duration'] = df['duration'].astype(str).str.extract(r'(\d+)').astype(float)
    df['release_year'] = df['release_year'].astype(int)
    return df

def writing(moments, col):
    print(f'For "{col}": Mean={moments[0]:.2f}, Std Dev={moments[1]:.2f}, Skewness={moments[2]:.2f}, Excess Kurtosis={moments[3]:.2f}.')
    print(f'Data is {"right" if moments[2] > 0 else "left" if moments[2] < 0 else "not"}-skewed and {"leptokurtic" if moments[3] > 0 else "platykurtic" if moments[3] < 0 else "mesokurtic"}.')

def main():
    df = pd.read_csv('data.csv')
    df.info()
    df = preprocessing(df)
    col = 'duration'
    plot_relational_plot(df)
    plot_statistical_plot(df)
    plot_categorical_plot(df)
    writing(statistical_analysis(df, col), col)

if __name__ == '__main__':
    main()
