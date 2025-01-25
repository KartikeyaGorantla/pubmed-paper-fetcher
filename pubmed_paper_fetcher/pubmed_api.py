import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
import pandas as pd
import re
import logging
from .config import PUBMED_API_KEY

class PubMedFetcher:
    def __init__(self, api_key: Optional[str] = PUBMED_API_KEY):
        self.api_key = api_key
        # Rest of the existing code remains the same

class PubMedFetcher:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def search_papers(self, query: str, max_results: int = 100) -> List[Dict]:
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "xml",
        }
        if self.api_key:
            search_params["api_key"] = self.api_key

        try:
            response = requests.get(
                f"{self.BASE_URL}/esearch.fcgi", params=search_params
            )
            response.raise_for_status()

            # Extract PubMed IDs
            root = ET.fromstring(response.content)
            id_list = [id_elem.text for id_elem in root.findall(".//IdList/Id")]

            # Fetch details for each ID
            return self._fetch_paper_details(id_list)

        except requests.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return []

    def _fetch_paper_details(self, id_list: List[str]) -> List[Dict]:
        details_params = {"db": "pubmed", "id": ",".join(id_list), "retmode": "xml"}

        try:
            response = requests.get(
                f"{self.BASE_URL}/efetch.fcgi", params=details_params
            )
            response.raise_for_status()

            root = ET.fromstring(response.content)
            papers = []

            for article in root.findall(".//PubmedArticle"):
                paper = self._parse_article(article)
                if paper:
                    papers.append(paper)

            return papers

        except requests.RequestException as e:
            self.logger.error(f"Details fetch failed: {e}")
            return []

    def _parse_article(self, article: ET.Element) -> Optional[Dict]:
        
        try:
            # Extract title
            title_elem = article.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else "No Title"

            # Extract publication date
            pub_date_elem = article.find(".//PubDate")
            pub_date = self._parse_publication_date(pub_date_elem)

            # Extract authors
            authors = self._extract_authors(article)

            return {
                "pubmed_id": article.find(".//PMID").text,
                "title": title,
                "publication_date": pub_date,
                "authors": authors,
            }

        except Exception as e:
            self.logger.warning(f"Error parsing article: {e}")
            return None

    def _parse_publication_date(self, pub_date_elem: Optional[ET.Element]) -> str:
        """Parse publication date from XML element."""
        if pub_date_elem is None:
            return "Unknown"

        year_elem = pub_date_elem.find("Year")
        month_elem = pub_date_elem.find("Month")

        year = year_elem.text if year_elem is not None else "Unknown"
        month = month_elem.text if month_elem is not None else "Unknown"

        return f"{month} {year}"
    def _extract_authors(self, article: ET.Element) -> List[Dict]:
        authors = []
        corresponding_author = None

        for author_elem in article.findall('.//Author'):
            try:
                last_name = author_elem.findtext('.//LastName', 'Unknown')
                first_name = author_elem.findtext('.//ForeName', '')
                
                # Extract affiliation
                affiliation_elem = author_elem.find('.//Affiliation')
                affiliation = affiliation_elem.text if affiliation_elem is not None else ""
                
                # Try extracting email from affiliation using regex
                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                                        affiliation or '', re.IGNORECASE)
                email = email_match.group(0) if email_match else ""
                
                # Check if this is a corresponding author
                author_is_corresponding = author_elem.find('.//CollectiveName') is not None
                
                author_info = {
                    'name': f"{first_name} {last_name}".strip(),
                    'affiliation': affiliation,
                    'email': email
                }
                
                authors.append(author_info)
                
                # Prioritize corresponding author
                if author_is_corresponding or not corresponding_author:
                    corresponding_author = author_info
            
            except Exception as e:
                self.logger.warning(f"Error extracting author: {e}")
        
        return authors