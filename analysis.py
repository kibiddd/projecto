import concurrent.futures
from url import url_analysis
from domain import domain_analysis
from cont import content_analysis


# Assume url_analysis, domain_analysis, and content_analysis are already defined functions
def analysis():
    # Result dictionary to store the outputs
    results = {}

    # Using ThreadPoolExecutor to run these tasks concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks to the thread pool
        futures = {
            "url_analysis": executor.submit(url_analysis),
            "domain_analysis": executor.submit(domain_analysis),
            "content_analysis": executor.submit(content_analysis)
        }

        # Wait for all tasks to complete and collect results
        for task_name, future in futures.items():
            try:
                # Store the result of each task
                results[task_name] = future.result()
            except Exception as e:
                # Handle exceptions if a task fails
                results[task_name] = f"Error: {e}"

    # Print the results
    for task, result in results.items():
        print(f"{task}: {result}")
    return results


if __name__ == "__main__":
    analysis()