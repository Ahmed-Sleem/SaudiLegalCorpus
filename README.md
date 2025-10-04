# ArabicLegalCorpus

This repository hosts the dataset introduced in the paper:

**"Practical Framework for Arabic Legal Retrieval-Augmented Generation models"**  
by *Ahmed Sleem*, *Nihal Ahmed Adly* (E-JUST, 2025)

---

## 📖 Dataset Overview
ArabicLegalCorpus is the **largest open structured Arabic legal dataset** to date.  
It contains **13,812 legal provisions** extracted from **292 Saudi statutes** (10.9 MB), along with unstructured sources, URLs, and preprocessing scripts.  

The dataset has been curated from the official Saudi legal portal ([laws.boe.gov.sa](https://laws.boe.gov.sa)) and extensively preprocessed using an Arabic-specific normalization pipeline.  

---

## 📂 Repository Structure

```text
ArabicLegalCorpus/
│
├── dataset/
│   ├── articles_laws.csv                   # Structured legal articles
│   ├── decisions_laws.csv                  # Legal decisions dataset
│   ├── unstructured_laws.csv               # Raw unstructured scraped texts
│   ├── unstructured_laws_dataset_sample.txt# Sample of raw dataset (text)
│
├── extras/
│   ├── legal_dataset_unstructured_whole_text.txt # Large raw unstructured text dump
│   ├── saudi_laws_urls.csv                       # List of official source URLs
│
├── python processing/
│   ├── analysis.py                       # Dataset statistics & analysis
│   ├── merged.py                         # Script for merging different CSVs
│   ├── structured.py                     # Preprocessing & structuring pipeline
│
├── separated_law_md_documents/           # Individual statutes in Markdown
│   ├── part 1/ (100 MD files)
│   ├── part 2/ (100 MD files)
│   ├── part 3/ (100 MD files)
│   ├── القانون (النظام) الموحد للتعدين لدول مجلس التعاون.md
│   ├── النظام الأساسي للحكم.md
│   ├── النظام الأساسي لمركز المعلومات الجنائية...md
│   ├── ...
│
├── LICENSE
└── README.md

```

---

## ⚖️ Dataset Details

### **Structured CSV Files**
- **`articles_laws.csv`** → 13,812 provisions across 292 statutes, with columns:
  - `law_title`: Title of the statute
  - `rule`: Article identifier
  - `text`: Full Arabic legal text
  - `url`: Official source (56% coverage)  
- **`decisions_laws.csv`** → Complementary legal decisions dataset.  
- **`unstructured_laws.csv`** → Unprocessed scraped texts for reproducibility.  

### **Unstructured Sources**
- `unstructured_laws_dataset_sample.txt` → Example of raw unstructured articles.  
- `legal_dataset_unstructured_whole_text.txt` → Complete concatenated raw text (pre-normalization).  
- `saudi_laws_urls.csv` → URLs from the official Saudi legal database.  

### **Scripts**
- **`analysis.py`** → Generates statistics (article counts, vocab distribution, text length analysis).  
- **`merged.py`** → Combines different CSVs into a unified dataset.  
- **`structured.py`** → Implements preprocessing pipeline.  

### **Separated Markdown Files**
- Each statute is stored as a Markdown document.  
- Divided into **Part 1, Part 2, Part 3**, each containing ~100 statutes.  
- Filenames are in Arabic (statute titles).  

---

## 📊 Dataset Statistics
- **Total entries**: 13,812  
- **Unique statutes**: 292  
- **Size**: 10.9 MB  
- **Average words/article**: 60.17  
- **Max length**: 1,336 words  
- **Repealed articles preserved**: 15  
- **Amendments included**: 636  
- **Duplicate entries**: 0  

**Coverage examples**:  
- Commercial Law → 846 articles  
- Civil Transactions Law → 721 articles  
- Labor Law → 368 articles  
- Companies Law → 281 articles  

---

## 📑 Citation
If you use this dataset, please cite our paper:

```bibtex
@article{sleem2025arabiclegalrag,
  title={Practical Framework for Arabic Legal Retrieval-Augmented Generation models},
  author={Sleem, Ahmed and Adly, Nihal Ahmed},
  year={2025}
}

```

---

## 📜 License
This dataset is released under the Creative Commons Attribution 4.0 International (CC-BY 4.0) License.
You are free to share and adapt the dataset, provided you give appropriate credit.

