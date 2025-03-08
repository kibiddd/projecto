import requests
from dataset import load_dataset


def analyze_and_log_urls(urls, output_file):
    """Processes and writes each URL's analysis result to the output file."""
    with open(output_file, "w", encoding="utf-8") as file:
        for idx, url in enumerate(urls, start=1):
            print(f"Analyzing URL {idx}/{len(urls)}: {url}")
            result = url_analysis_stub(url)  # Replace with `url_analysis(url)`

            # Write the result in JSON-like format to the output file
            file.write(f"{result}\n")

            # Optional: Log to console to monitor real-time progress
            print(f"Result logged for URL {idx}.")


if __name__ == "__main__":
    dataset_url = "https://phish.co.za/latest/phishing-links-ACTIVE.txt"
    urls = load_dataset(dataset_url)

    if urls:
        analyze_and_log_urls(urls, "phishing_results.txt")
        print("Analysis completed. Results saved to 'phishing_results.txt'.")