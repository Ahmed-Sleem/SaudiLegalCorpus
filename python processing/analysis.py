import sys
import pandas as pd
import numpy as np
from collections import Counter
import re
from math import log

def analyze_csv(file_path):
    df = pd.read_csv(file_path)

    print("="*80)
    print(f"📊 Advanced Analysis Report for: {file_path}")
    print("="*80)

    # 1. Shape
    print(f"Number of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}\n")

    # 2. Columns info
    print("Column Names and Data Types:")
    print(df.dtypes, "\n")

    # 3. Missing values
    print("Missing Values per Column:")
    print(df.isnull().sum(), "\n")

    # 4. Descriptive stats
    num_cols = df.select_dtypes(include=[np.number])
    cat_cols = df.select_dtypes(include=[object])

    if not num_cols.empty:
        print("Descriptive Statistics (numerical):")
        print(num_cols.describe().T, "\n")
    else:
        print("No numerical columns found.\n")

    if not cat_cols.empty:
        print("Descriptive Statistics (categorical):")
        print(cat_cols.describe().T, "\n")
    else:
        print("No categorical columns found.\n")

    # 5. Value counts
    if not cat_cols.empty:
        print("Top values for categorical columns:")
        for col in cat_cols.columns:
            print(f"\nColumn: {col}")
            print(df[col].value_counts().head(10))
    print()

    # 6. Correlation matrix
    if num_cols.shape[1] > 1:
        print("Correlation Matrix (numerical columns):")
        print(num_cols.corr(), "\n")

    # 7. Duplicate rows
    print(f"Duplicate rows: {df.duplicated().sum()}\n")

    # 8. Top words across all text columns
    if not cat_cols.empty:
        words = []
        for col in cat_cols:
            words.extend(
                re.findall(r'\w+', ' '.join(df[col].dropna().astype(str)).lower())
            )
        counter = Counter(words)
        print("Top 20 most repeated words across text columns:")
        for word, freq in counter.most_common(20):
            print(f"{word}: {freq}")
        print()

    # 9. Outlier detection (basic z-score rule)
    if not num_cols.empty:
        print("Outlier Detection (values beyond 3*std):")
        for col in num_cols.columns:
            mean, std = df[col].mean(), df[col].std()
            if std > 0:
                outliers = df[(df[col] < mean - 3*std) | (df[col] > mean + 3*std)]
                print(f"{col}: {len(outliers)} potential outliers")
        print()

    # 10. Correlation with target (if exists)
    if 'target' in df.columns and df['target'].dtype in [np.int64, np.float64]:
        print("Correlation of features with 'target':")
        print(num_cols.corrwith(df['target']), "\n")

    # 11. Word length & sentence length stats
    if not cat_cols.empty:
        print("Word and sentence length stats:")
        for col in cat_cols:
            lengths = df[col].dropna().astype(str).apply(lambda x: len(x.split()))
            print(f"{col} - Avg words: {lengths.mean():.2f}, Max words: {lengths.max()}")
        print()

    # 12. Lightweight TF-IDF (sample docs only)
    if not cat_cols.empty:
        print("TF-IDF Term Importance (Top terms for 3 sample docs):")
        first_text_col = list(cat_cols)[0]   # ✅ safe access
        sample_docs = [str(x) for x in df[first_text_col].dropna().head(10)]
        if sample_docs:
            N = len(sample_docs)
            vocab = set(re.findall(r'\w+', ' '.join(sample_docs).lower()))
            idf = {
                term: log(N / (1 + sum(1 for d in sample_docs if term in d.lower())))
                for term in vocab
            }
            for idx, doc in enumerate(sample_docs[:3]):
                tf = Counter(re.findall(r'\w+', doc.lower()))
                if len(doc.split()) > 0:
                    tfidf = {t: (tf[t] / len(doc.split())) * idf[t] for t in tf}
                    top_terms = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:10]
                    print(f"\nDoc idx {idx} top tf-idf terms:")
                    for term, score in top_terms:
                        print(f"   {term}: {score:.2f}")

    print("\n✅ Analysis complete (heavy steps removed).")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_csv.py <path_to_csv>")
    else:
        analyze_csv(sys.argv[1])
