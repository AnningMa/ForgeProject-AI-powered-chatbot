import re
import pandas as pd
import numpy as np
import spacy 
from spacy.matcher import Matcher, PhraseMatcher
from fincial_analysis import clean_data, calculate_financial_ratios

class FinancialChatbot:
    def __init__(self, df):
        self.nlp = spacy.load("en_core_web_sm")
        try:
            self.data = df.set_index(["Company", "Year"])
        except KeyError:
            print("Error: DataFrame must contain 'Company' and 'Year' columns.")
            return
        
        self.companies = list(df["Company"].unique())
        self.state = {
            "current_company": None,
            "current_metric": None,
            "current_year": None
        }
        
        self.metric_map = {
            "total revenue": "Total Revenue",
            "revenue": "Total Revenue",
            "sales": "Total Revenue",
            "top line": "Total Revenue",
            "net income": "Net Income",
            "profit": "Net Income",
            "earnings": "Net Income",
            "bottom line": "Net Income",
            "debt ratio": "Debt Ratio (%)",
            "leverage": "Debt Ratio (%)",
            "debt": "Debt Ratio (%)",
            "roa": "ROA (%)",
            "return on assets": "ROA (%)",
            "cfo": "CFO / Net Income",
            "cash flow quality": "CFO / Net Income",
            "current ratio": "Current Ratio",
            "liquidity": "Current Ratio"
            # ......
        }
        
        self.matcher = Matcher(self.nlp.vocab)
        self.phrase_matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        
        year_pattern = [{'SHAPE': 'dddd'}]
        self.matcher.add("DATE", [year_pattern])
        
        company_patterns = [self.nlp.make_doc(c) for c in self.companies]
        self.phrase_matcher.add("ORG", company_patterns)
        
        metric_patterns = [self.nlp.make_doc(text) for text in self.metric_map.keys()]
        self.phrase_matcher.add("FIN_METRIC", metric_patterns)
    
    def _format_value(self, value, metric):
        if pd.isna(value):
            return "N/A (Data not available)"
        if "(%)" in metric or "Ratio" in metric or "/" in metric:
            return f"{value:.2f}%"
        if abs(value) > 1_000_000_000:
            return f"${value / 1_000_000_000:.2f} Billion"
        if abs(value) > 1_000_000:
            return f"${value / 1_000_000:.2f} Million"
        return f"${value:,.2f}"
    
    def chat(self, user_query):
        doc = self.nlp(user_query)
        matches = self.matcher(doc) + self.phrase_matcher(doc)
        
        found_company = False
        found_metric = False
        found_year = False

        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id]
            span = doc[start:end] # 获取匹配到的文本
            
            if label == "DATE":
                self.state["current_year"] = int(span.text)
                found_year = True
            
            if label == "ORG":
                self.state["current_company"] = span.text 
                found_company = True
            
            if label == "FIN_METRIC":
                self.state["current_metric"] = self.metric_map[span.text.lower()]
                found_metric = True
        
        if not self.state["current_company"]:
            return "Which company are you asking about?"

        if not self.state["current_metric"]:
            return f"What financial metric would you like for {self.state['current_company']}?"
        
        if not found_year and not self.state["current_year"]:
            latest_year = self.data.loc[self.state["current_company"]].index.max()
            self.state["current_year"] = latest_year
            print(f"(Debug: No year provided, defaulting to {latest_year})")
        
        company = self.state["current_company"]
        year = self.state["current_year"]
        metric = self.state["current_metric"]
        
        try:
            value = self.data.loc[(company, year), metric]
            formatted_value = self._format_value(value, metric)
            response = f"Here is the data: {company}'s {metric} in {year} was {formatted_value}."
        
            self.state["current_year"] = None 
            
            return response

        except KeyError:
            return f"I'm sorry, I could not find data for {metric} for {company} in {year}."
        except Exception as e:
            return f"An unexpected error occurred: {e}"
        

if __name__ == "__main__":
    df = pd.read_excel("financial_data.xlsx")
    df = clean_data(df)
    df = calculate_financial_ratios(df)
    
    bot = FinancialChatbot(df)
    def ask_bot(query):
        response = bot.chat(query)
        print("User:", query)
        print("Bot:", response)
        print("-" * 40)
    
    # 1. Test synonyms ("profit" and "leverage")
    ask_bot("What was Apple's profit in 2023?")
    ask_bot("What about their leverage?") # Should remember "Apple", match "leverage", and use latest year (2024)

    # 2. Test state management
    ask_bot("show me Microsoft's sales for 2024")
    ask_bot("what about 2022?") # Should remember "Microsoft" and "Total Revenue", update year to 2022
    ask_bot("how about their ROA?") # Should remember "Microsoft", match "ROA", and use latest year (2024)
    
    # 3. Test error handling
    ask_bot("What is the liquidity for Tesla?") # Matches "liquidity" -> "Current Ratio"
    ask_bot("What about Google?") # "Google" is not in the company list
    
    
    print ("Chatbot testing complete.")
