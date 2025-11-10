# ============================================
# 🧬 Interactive Biological Sequence Visualizer
# ============================================

# 🧩 STEP 1: Required installations (run these once in VS Code terminal)
# pip install streamlit biopython pandas plotly

# 🧩 STEP 2: Imports
import streamlit as st
from Bio import SeqIO
import pandas as pd
import plotly.express as px
from io import StringIO

# 🧩 STEP 3: Helper Functions

def analyze_sequences(uploaded_file):
    """
    Reads FASTA file and returns a DataFrame containing
    sequence IDs, lengths, and GC content.
    """
    seq_data = []

    try:
        sequences = list(SeqIO.parse(uploaded_file, "fasta"))
        for record in sequences:
            seq_id = record.id
            seq_len = len(record.seq)
            gc_content = (record.seq.count("G") + record.seq.count("C")) / seq_len * 100
            seq_data.append({"Sequence ID": seq_id, "Length": seq_len, "GC Content (%)": gc_content})
        return pd.DataFrame(seq_data)
    except Exception as e:
        st.error(f"Error analyzing sequences: {e}")
        return None

def plot_length_distribution(df):
    """Plot length distribution"""
    fig = px.histogram(df, x="Length", nbins=20, title="Sequence Length Distribution")
    st.plotly_chart(fig)

def plot_gc_content(df):
    """Plot GC content"""
    fig = px.scatter(df, x="Length", y="GC Content (%)", title="GC Content vs Sequence Length", hover_data=["Sequence ID"])
    st.plotly_chart(fig)

# 🧩 STEP 4: Streamlit App UI

st.set_page_config(page_title="Biological Sequence Visualizer", layout="wide")

st.title("🧫 Interactive Biological Sequence Visualizer")
st.markdown("Upload a FASTA file to explore its biological sequence data interactively.")

uploaded_file = st.file_uploader("📂 Upload your FASTA file", type=["fasta", "fa"])

if uploaded_file is not None:
    df = analyze_sequences(uploaded_file)

    if df is not None:
        st.success("✅ File uploaded and analyzed successfully!")
        st.subheader("📊 Sequence Summary Table")
        st.dataframe(df)

        st.subheader("📈 Visualizations")
        col1, col2 = st.columns(2)
        with col1:
            plot_length_distribution(df)
        with col2:
            plot_gc_content(df)
else:
    st.info("👆 Please upload a FASTA file to begin.")