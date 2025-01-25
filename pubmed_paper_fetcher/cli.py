import click
import logging
import pandas as pd
from typing import Optional

from .pubmed_api import PubMedFetcher
from .author_filter import AuthorFilter

@click.command()
@click.argument('query', type=str)
@click.option('-h', '--help', 'show_help', is_flag=True, help='Display usage instructions')
@click.option('-d', '--debug', is_flag=True, help='Enable debug logging')
@click.option('-f', '--file', type=click.Path(), help='Specify filename to save results')
@click.option('-m', '--max-results', default=100, help='Maximum number of results to fetch')
def main(query: str, show_help: bool, debug: bool, file: Optional[str], max_results: int):
    # Handle help option
    if show_help:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s'
    )
    logger = logging.getLogger(__name__)

    try:
        # Initialize fetcher
        fetcher = PubMedFetcher()
        
        # Search and fetch papers
        logger.info(f"Searching PubMed with query: {query}")
        papers = fetcher.search_papers(query, max_results)
        
        # Filter non-academic papers
        filtered_papers = AuthorFilter.filter_non_academic_papers(papers)
        
        # Prepare DataFrame
        if filtered_papers:
            # Transform data for output
            csv_data = []
            for paper in filtered_papers:
                csv_row = {
                    'PubMed ID': paper.get('pubmed_id', 'N/A'),
                    'Title': paper.get('title', 'N/A'),
                    'Publication Date': paper.get('publication_date', 'N/A'),
                    'Non-Academic Authors': ', '.join([
                        author['name'] for author in paper.get('non_academic_authors', [])
                    ]),
                    'Company Affiliations': ', '.join([
                        author['affiliation'] for author in paper.get('non_academic_authors', [])
                    ]),
                    'Corresponding Author Email': ', '.join([
                        author.get('email', '') for author in paper.get('non_academic_authors', []) 
                        if author.get('email')
                    ])
                }
                csv_data.append(csv_row)
            
            df = pd.DataFrame(csv_data)
            
            # Output handling
            if file:
                df.to_csv(file, index=False)
                logger.info(f"Results saved to {file}")
            else:
                print(df.to_string())
        else:
            logger.warning("No papers found matching the criteria.")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == '__main__':
    main()