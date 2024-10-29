import json
import pandas as pd
import os

def find_multiqc_file(run_path):
    """
    Recursively searches for the multiqc_data.json file within the given directory.

    Parameters:
    run_path (str): The path to the directory where the search should begin.

    Returns:
    str: The full path to the multiqc_data.json file, or None if not found.
    """
    for root, dirs, files in os.walk(run_path):
        if "multiqc_data.json" in files:
            return os.path.join(root, "multiqc_data.json")
    return None

def parse_multiqc_statistics(run_path):
    """
    Searches for the MultiQC JSON file in the given run directory and its subdirectories, 
    and returns a pandas DataFrame with all statistics.

    Parameters:
    run_path (str): The path to the directory containing the MultiQC output.

    Returns:
    pd.DataFrame: A DataFrame containing all the parsed statistics, or None if the file is not found.
    """
    run_name = run_path.strip("/").split("/")[-1]
    # Find the MultiQC JSON file recursively
    multiqc_file_path = find_multiqc_file(run_path)
    
    if multiqc_file_path is None:
        raise FileNotFoundError(f"The file multiqc_data.json was not found in the directory {run_path} or its subdirectories.")
    
    try:
        # Load the MultiQC JSON data
        with open(multiqc_file_path, 'r') as f:
            multiqc_data = json.load(f)
        
        # Initialize an empty list to hold the parsed data
        data = []
        
        # Iterate over each module (e.g., FastQC, Samtools, etc.) in the report
        for module_name, module_data in multiqc_data['report_saved_raw_data'].items():
            for sample_name, sample_stats in module_data.items():
                # Flatten the sample statistics and include the module and sample name
                flat_stats = {'Module': module_name, 'Sample': sample_name}
                flat_stats.update(sample_stats)
                data.append(flat_stats)
        
        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(data)
        # Table by lane
        by_lane = df.loc[df["Module"]=="multiqc_bcl2fastq_bylane"].dropna(axis=1, how='all')
        by_lane = by_lane[["Sample", "total", "undetermined", "unknown_barcodes"]]
        by_lane["run_name"] = run_name
        # Table by samples
        by_samples = df.loc[df["Module"]=="multiqc_bcl2fastq_bysample"].dropna(axis=1, how='all')
        by_samples = by_samples[["Sample", "total"]]
        by_samples["run_name"] = run_name
        # Summary
        summary = by_lane.sum(numeric_only=True)
        summarydf = pd.DataFrame({"run_name": [run_name],
                                  "total": [summary.iloc[0]],
                                  "undetermined": [summary.iloc[1]],
                                  "undetermined_pct": [summary.iloc[1]/(summary.iloc[0] + summary.iloc[1])]})
        return summarydf, by_lane, by_samples
    
    except Exception as e:
        print(f"An error occurred while parsing MultiQC statistics: {e}")
        return None

if __name__ == '__main__':
    summarydf, by_lane, by_samples = parse_multiqc_statistics("/data/fastq/240708_A01742_0257_AHCLLVDRX5/")
    print(summarydf.columns)
    # print(df[["Sample", "undetermined", "unknown_barcodes"]])