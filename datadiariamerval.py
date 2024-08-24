import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import streamlit as st
from matplotlib.ticker import FuncFormatter

# Function to format large numbers (e.g., 1,000 as 1K, 1,000,000 as 1M)
def format_large_number(num):
    if num >= 1_000_000_000:
        return f'{num / 1_000_000_000:.1f}B'
    elif num >= 1_000_000:
        return f'{num / 1_000_000:.1f}M'
    elif num >= 1_000:
        return f'{num / 1_000:.1f}K'
    else:
        return str(num)

# Function to create a bubble chart with different colors and labels
def create_bubble_chart(x, y, size, labels, xlabel, ylabel, title):
    plt.figure(figsize=(14, 10))
    
    # Ensure the size is positive
    size = np.abs(size)
    
    # Generate a scatter plot with varying bubble colors
    cmap = plt.get_cmap("viridis")
    norm = plt.Normalize(min(size), max(size))
    colors = cmap(norm(size))
    
    # Plot bubbles
    scatter = plt.scatter(x=x, y=y, s=size, c=colors, alpha=0.6, edgecolors="w", linewidth=2)
    
    # Add labels with arrows/lines
    for i, label in enumerate(labels):
        plt.annotate(label,
                     (x[i], y[i]),
                     textcoords="offset points",
                     xytext=(10, 10),  # Distance from the point
                     ha='center',
                     arrowprops=dict(arrowstyle="->", lw=1.5, color='black'))
    
    # Customize and format the plot
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.grid(True)
    
    # Formatter for large numbers
    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: format_large_number(x)))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: format_large_number(y)))
    
    st.pyplot(plt)  # Display the plot in Streamlit

# Example usage with sample data (replace this with your data-fetching code)
# Simulated data for demonstration purposes
x = np.random.rand(10) * 100  # Random price variation
y = np.random.rand(10) * 1e6  # Random volume*price
size = y  # Bubble size based on volume*price
labels = [f'Ticker {i}' for i in range(10)]  # Simulated labels

# Create the bubble chart
create_bubble_chart(x, y, size, labels, 'Price Variation (%)', 'Volume * Price', 'Volume * Price vs. Price Variation')
