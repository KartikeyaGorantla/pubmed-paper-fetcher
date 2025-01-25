import re
from typing import List, Dict


class AuthorFilter:
    PHARMA_KEYWORDS = [
        "pharmaceutical",
        "biotech",
        "pharma",
        "drug discovery",
        "biopharmaceutical",
        "therapeutics",
        "laboratories",
        "research institute",
        "innovation center",
    ]

    NON_ACADEMIC_DOMAINS = [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "company.com",
        "corp.com",
        "inc.com",
    ]

    @classmethod
    def is_non_academic_author(cls, author: Dict) -> bool:
        """
        Determine if an author is from a non-academic institution.

        Args:
            author (Dict): Author details dictionary

        Returns:
            bool: True if likely non-academic, False otherwise
        """
        affiliation = author.get("affiliation", "").lower()

        # Check for pharma keywords
        if any(keyword in affiliation for keyword in cls.PHARMA_KEYWORDS):
            return True

        # Check email domains (if available)
        email = re.search(
            r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b",
            affiliation,
            re.IGNORECASE,
        )
        if email:
            domain = email.group(1).lower()
            if any(non_academic in domain for non_academic in cls.NON_ACADEMIC_DOMAINS):
                return True

        # Advanced company detection
        company_patterns = [
            r"\b[A-Z][a-z]+ (Inc\.|LLC|Corporation|Ltd\.)\b",
            r"\b(Pharmaceuticals|Therapeutics|Laboratories)\b",
        ]
        if any(
            re.search(pattern, affiliation, re.IGNORECASE)
            for pattern in company_patterns
        ):
            return True

        return False

    @classmethod
    def filter_non_academic_papers(cls, papers: List[Dict]) -> List[Dict]:
        """
        Filter papers to include only those with non-academic authors.

        Args:
            papers (List[Dict]): List of papers with author details

        Returns:
            List[Dict]: Filtered list of papers
        """
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
