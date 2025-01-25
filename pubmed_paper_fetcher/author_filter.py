import re
from typing import List, Dict


class AuthorFilter:
    @classmethod
    def is_non_academic_author(cls, author: Dict) -> bool:
        
        affiliation = author.get("affiliation", "").lower()

        # Check for academic keywords to EXCLUDE
        academic_keywords = [
            "university",
            "college",
            "department of",
            "school of",
            "faculty of",
            "research center",
            "institute of",
            "academic medical center",
            "laboratory",
            "lab of",
            "campus",
        ]

        # If ANY academic keyword is found, return False
        if any(keyword in affiliation for keyword in academic_keywords):
            return False

        # Additional non-academic detection
        pharma_keywords = [
            "pharmaceutical",
            "biotech",
            "pharma",
            "drug discovery",
            "biopharmaceutical",
            "therapeutics",
            "innovations",
            "corp",
            "inc.",
        ]

        # Return True if pharma keywords are found
        return any(keyword in affiliation for keyword in pharma_keywords)

    @classmethod
    def filter_non_academic_papers(cls, papers: List[Dict]) -> List[Dict]:
        filtered_papers = []

        for paper in papers:
            non_academic_authors = [
                author
                for author in paper.get("authors", [])
                if cls.is_non_academic_author(author)
            ]

            if non_academic_authors:
                paper["non_academic_authors"] = non_academic_authors
                filtered_papers.append(paper)

        return filtered_papers
