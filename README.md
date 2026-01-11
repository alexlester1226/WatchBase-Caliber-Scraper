# Caliber Intel: LLM-Assisted Horology Data Pipeline

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Data](https://img.shields.io/badge/Dataset-1000+_Entries-orange.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)

## 🎯 Project Purpose
This project automates the collection, normalization, and analysis of high-end watch movement data. By leveraging **LLM-generated Python scraping logic**, I successfully extracted and structured data for approximately **1,000 watch calibers** from WatchBase.com. 

The result is a high-quality dataset designed for horological research, market analysis, and movement comparison.


## 📊 Data Points Captured
The engine extracts and normalizes the following technical specifications:
* **Caliber Identity:** Name and Brand.
* **Architecture:** Movement Type (Manual, Automatic, Quartz).
* **Performance:** Beat Rate (VPH) and Power Reserve (Hours).
* **Complexity:** Detailed list of Complications.

## 🛠️ Technical Workflow
### 1. Extraction (LLM-Assisted Scraping)
* Used LLM prompting to iterate and optimize Python-based scraping scripts.
* Implemented **Selenium/BeautifulSoup** to navigate complex web architectures and bypass common anti-scraping hurdles.

### 2. Processing & Normalization
* **Data Cleaning:** Handled inconsistent units (e.g., converting varied power reserve formats).
* **Normalization:** Standardized brand names and movement categories using **Pandas**.

### 3. Exploratory Analysis
* Conducted initial analysis to identify patterns in beat rates and complications across different luxury brands.



## 🚀 Key Learnings
* **Prompt Engineering for Code:** Learned to use LLMs as a "force multiplier" to generate boilerplate scraping logic, which was then manually refined for edge-case handling.
* **Tool Selection:** Evaluated various scraping libraries to find the optimal balance between speed and reliability for 1,000+ entries.
* **Data Integrity:** Developed techniques to ensure a "structured, high-quality dataset" even when the source HTML was inconsistent.

## 📂 Repository Contents
* `trulux_project.py`: The core extraction, cleaning and plotting engine.
* `raw_data.csv`: The final structured output (Sample).
* `cleaned_data.csv`: The final structured output (Sample).
* `TruLux.ScrapingProject.Report.pdf`: A detailed breakdown of methodology and findings.
* `*.png`: PNG images of different plotted graphs and findings

---
**Developed by Alex Lester** *Passionate about turning raw web data into actionable business intelligence.
[Visit Personal Website](https://www.alexlester.org)
[Visit LinkedIn](https://www.linkedin.com/in/alex-lester-4a4a93236/)
