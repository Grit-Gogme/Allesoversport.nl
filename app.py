import streamlit as st
import requests
from bs4 import BeautifulSoup

def scrape_pages(search_query):
    base_url = "https://www.allesoversport.nl"
    search_url = f"{base_url}/?s={'+'.join(search_query.split())}"

    # Debug: Laat de zoek-URL zien
    st.write(f"Zoek-URL: {search_url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        st.error(f"Kan de website niet bereiken (statuscode: {response.status_code}).")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Zoek artikelen
    articles = []
    for link in soup.find_all("a", href=True):
        url = link["href"]
        title = link.text.strip()
        if "allesoversport.nl" in url and title:
            articles.append({"url": url, "title": title})
    
    if not articles:
        st.warning("Geen artikelen gevonden. Controleer de zoekterm of de website-structuur.")
    return articles

st.title("AllesOverSport.nl Zoektool")

search_query = st.text_input("Zoek naar artikelen (bijv. 'sport en gezondheid'):")

if st.button("Zoek Artikelen") and search_query:
    st.write(f"Zoeken naar: **{search_query}**")
    articles = scrape_pages(search_query)
    
    for article in articles:
        st.write(f"- [{article['title']}]({article['url']})")
