import seaborn as sns
import matplotlib.pyplot as plt

def univariate_analysis(df, column):
    """Plot univariate analysis for a given column."""
    plt.figure(figsize=(8, 6))
    sns.histplot(df[column], kde=True)
    plt.title(f'Distribution of {column}')
    plt.show()

def bivariate_analysis(df, feature, target):
    """Plot bivariate analysis between a feature and target variable."""
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=target, y=feature, data=df)
    plt.title(f'{feature} vs {target}')
    plt.show()
