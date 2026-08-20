import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_categorical_relationship(df, cat_1, cat_2, target):
    # Calculate counts for cat_1 and cat_2
    counts = df.groupby([cat_1, cat_2])[target].size().reset_index(name='count')
    
    # Calculate proportions for cat_2 within each cat_1 category
    counts['proportion'] = counts['count'] / counts.groupby(cat_1)['count'].transform('sum')
    
    # Calculate mean target for cat_1 and cat_2
    target_mean = df.groupby([cat_1, cat_2])[target].mean().reset_index(name='mean_target')
    
    # Pivot data for bar plot
    bar_data = counts.pivot(index=cat_1, columns=cat_2, values='count').fillna(0)
    proportion_data = counts.pivot(index=cat_1, columns=cat_2, values='proportion').fillna(0)
    
    # Set up the figure
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Define a consistent color palette
    colors = sns.color_palette('colorblind', n_colors=bar_data.columns.size)
    color_map = dict(zip(bar_data.columns, colors))
    
    # Stacked bar plot using actual counts for cat_1
    for category in bar_data.columns:
        ax1.bar(bar_data.index, bar_data[category], label=f'{category}', color=color_map[category], alpha=0.8, bottom=bar_data[bar_data.columns[:bar_data.columns.get_loc(category)]].sum(axis=1))
    
    ax1.set_ylabel('Count')
    ax1.set_xlabel(cat_1)
    ax1.set_title(f'{cat_1} vs {cat_2} with Mean {target}')
    ax1.tick_params(axis='x', rotation=45)  # Rotate x-axis labels
    
    # Secondary axis for mean target
    ax2 = ax1.twinx()
    for category in target_mean[cat_2].unique():
        cat_data = target_mean[target_mean[cat_2] == category]
        ax2.plot(cat_data[cat_1], cat_data['mean_target'], marker='o', label=f'Mean {target} ({category})', color=color_map[category])
    
    ax2.set_ylabel(f'Mean {target}')
    
    # Combine legends for bars and lines
    handles, labels = ax1.get_legend_handles_labels()
    line_handles, line_labels = ax2.get_legend_handles_labels()
    ax2.legend(handles + line_handles, labels + line_labels, title=cat_2, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()

# Example usage
# Assuming `df` is your DataFrame with columns "cat_1", "cat_2", and "target"
# plot_categorical_relationship(df, 'cat_1', 'cat_2', 'target')

def plot_cat2violin(df, categorical_col, numerical_col):
    # Calculate the mean of the numerical column for each category in the categorical column
    category_means = df.groupby(categorical_col)[numerical_col].mean().sort_values(ascending=False)
    
    # Create a new column with ordered categories
    df['sorted_category'] = pd.Categorical(df[categorical_col], categories=category_means.index, ordered=True)
    
    plt.figure(figsize=(10, 6))
    
    sns.violinplot(x='sorted_category', y=numerical_col, data=df)
    
    # Add a line connecting the mean points
    plt.plot(category_means.index, category_means.values, color='r', marker='o', linestyle='-')
    
    # Add mean values at the bottom, just above the x-axis
    for i, mean in enumerate(category_means.values):
        plt.text(i, df[numerical_col].min() - 1, f'{mean:.2f}', color='r', ha='center', va='top')
    
    plt.title(f'{numerical_col} Distribution by {categorical_col} (Sorted)')
    plt.xlabel(categorical_col)
    plt.ylabel(numerical_col)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.show()

    del df['sorted_category']

    print("we did some changes")

    print("we did even more chages")
    
    