This project, completed as part of a **The Forage Virtual Internship**, transforms dense, unstructured 10-K financial reports into an interactive, conversational insights tool.

The pipeline involves two major stages:
1.  **Financial Data Analysis:** Extracting, cleaning, and consolidating key financial metrics (e.g., Total Revenue, Net Income) and calculating growth indicators and performance ratios (e.g., Net Profit Margin, Debt Ratio).
2.  **NLP Chatbot System:** Building a stateful, NLP-driven chatbot using `spaCy` that allows users to query the consolidated financial data using natural language.

## 🚀 Key Features

* **Financial Data Pipeline:** Reads and processes complex financial data (simulated from 10-K filings) using `pandas` to create a clean, indexed database.
* **Intelligent Entity Extraction:** Uses `spaCy`'s `Matcher` and `PhraseMatcher` to robustly identify key entities from user queries:
    * **ORG (Organization):** e.g., "Apple", "Microsoft"
    * **DATE (Year):** e.g., "2023", "in 2022"
    * **FIN_METRIC (Financial Metric):** Handles a wide range of synonyms (e.g., "profit", "earnings", "bottom line" all map to `Net Income`; "leverage" maps to `Debt Ratio (%)`).
* **Stateful Conversation:** The chatbot remembers the context of the conversation (e.g., the company or metric being discussed) to allow for natural follow-up questions.
* **Dynamic Responses:** Formats financial data intelligently (e.g., `$211.92 Billion`, `52.30%`) for clean, human-readable answers.

## 🛠️ Tech Stack & Skills Demonstrated

* **Programming:** Python
* **Data Analysis & Manipulation:** Pandas, NumPy
* **Natural Language Processing (NLP):** spaCy (Entity Recognition, Matcher, PhraseMatcher)
* **Core Skills:**
    * Financial Data Analysis (Ratio Calculation, Trend Analysis)
    * Data Cleaning & Preparation
    * NLP-driven Intent Recognition
    * Chatbot State Management
    * Object-Oriented Programming (OOP)
