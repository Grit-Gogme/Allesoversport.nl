import streamlit as st
import requests
from bs4 import BeautifulSoup

# Functie om pagina's op basis van een zoekterm te scrapen
def scrape_pages(search_query):
    base_url = "https://www.allesoversport.nl"
    search_url = f"{base_url}/?s={'+'.join(search_query.split())}"
    
    # Haal de HTML op van de zoekpagina
    response = requests.get(search_url)
    if response.status_code != 200:
        st.error("Kan de website niet bereiken. Controleer de URL of probeer later opnieuw.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Zoek alle links in de zoekresultaten
    articles = []
    for link in soup.find_all("a", href=True):
        url = link["href"]
        title = link.text.strip()
        if base_url in url and title:  # Filter relevante links
            articles.append({"url": url, "title": title})
    
    return articles

# Functie om samenvattingen van artikelen te maken
def summarize_article(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return "Artikel kan niet worden geladen."

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        summary = " ".join([p.text for p in paragraphs[:3]])  # Neem de eerste 3 paragrafen
        return summary
    except Exception as e:
        return f"Fout bij het laden van de samenvatting: {e}"

# Streamlit-app interface
st.title("AllesOverSport.nl Zoektool")

# Gebruiker invoer via zoekbalk
search_query = st.text_input("Zoek naar artikelen (bijv. 'sport en gezondheid', 'kinderen zwemmen'):")

if st.button("Zoek Artikelen") and search_query:
    st.write(f"Zoeken naar artikelen met de term(en): **{search_query}**")
    
    articles = scrape_pages(search_query)
    
    if articles:
        st.write(f"**{len(articles)} artikelen gevonden**")
        
        for article in articles:
            with st.expander(article["title"]):
                summary = summarize_article(article["url"])
                st.write(summary)
                st.markdown(f"[Lees meer]({article['url']})")
    else:
        st.warning("Geen artikelen gevonden voor deze zoekopdracht.")
