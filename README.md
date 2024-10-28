# Job Crolling

This project is designed to scrape job postings from a given URL and output the results into a CSV file. The CSV file will include details such as the date, company name, and job title.

## Project Structurer

- `src/`: Contains the source code for the web crawler.
  - `crawler.py`: Main script to perform web crawling.
  - `utils.py`: Utility functions to support the crawler.
  
- `data/`: Directory where the output CSV file will be stored.
  - `output.csv`: The resulting CSV file with job postings.

- `requirements.txt`: Lists the Python dependencies required for the project.

- `README.md`: Documentation for the project.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ygh1254/Job_Crolling.git
   cd Job_Crolling
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the crawler script with the desired URL:
   ```bash
   python src/crawler.py --url "http://example.com/jobs"
   ```

2. The results will be saved in `data/output.csv`.

## Requirements

- Python 3.12.7
- Libraries specified in `requirements.txt` (e.g., BeautifulSoup, requests)

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements.

## License

This project is licensed under the MIT License.
