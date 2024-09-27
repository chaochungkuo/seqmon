# Seqmon

**A Lightweight Sequencing Monitor**

Seqmon is a web application built on Plotly Dash designed to monitor sequencing runs across multiple sequencers and analyze the statistics of demultiplexing processes. 

Seqmon parses through all the paths defined in `config.yaml` and collects the following information:

- **Run Statistics:** Aggregated from both BCL and MultiQC data.
- **Lane Statistics:** Extracted from MultiQC data.
- **Sample Statistics:** Also sourced from MultiQC data.

These statistics are saved under the `./data/` directory and can be updated when new data becomes available. Existing entries won’t be reloaded unless you manually remove the associated files.

![Screenshot of Seqmon](./assets/screenshot.png.png "Screenshot of Seqmon")

## Configuration

### Prerequisites

1. **Clone the Repository:**
   Begin by cloning the repository to a location where your data is stored:

   ```bash
   gh repo clone chaochungkuo/seqmon
   ```

2. **Adjust Configuration:**
   Update the configuration file located at `config/config.yaml` to reflect your environment.

   - **`bcl_paths`:** Paths to the BCL files from Illumina sequencers.
   - **`multiqc_paths`:** Paths where the `multiqc_data` directories can be found.

   The subfolders in these paths should correspond to the run IDs assigned by the Illumina sequencers.

   **Example Data Structure:**

   ```plaintext
   BCL outputs from Illumina Sequencers:
   - /data/raw/miseq1_M00818/240826_M00818_0927_000000000-KWWCM
   - /data/raw/miseq1_M00818/240902_M00818_0930_000000000-LNB62
   - /data/raw/miseq2_M04404/240708_M04404_0764_000000000-LMF2H
   - /data/raw/miseq2_M04404/240711_M04404_0765_000000000-LL9CJ
   - /data/raw/nextseq_NB501289/240815_NB501289_0844_AHT2CJBGXW
   - /data/raw/nextseq_NB501289/240820_NB501289_0846_AHH55LAFX7
   - /data/raw/novaseq_A01742/240815_A01742_0281_BHWL23DMXY
   - /data/raw/novaseq_A01742/240819_A01742_0283_BHGL5GDRX5

   Demultiplexing folders containing multiqc_data:
   - /data/fastq/240404_A01742_0223_AH3VMHDRX5
   - /data/fastq/240408_A01742_0224_AH3W5YDRX5
   - /data/fastq/240408_M04404_0742_000000000-LHTLJ
   - /data/fastq/240410_NB501289_0799_AHNVNJBGXV
   ```

   Update your `config.yaml` accordingly:

   ```yaml
   bcl_paths:
     - /data/raw/miseq1_M00818
     - /data/raw/miseq2_M04404
     - /data/raw/nextseq_NB501289
     - /data/raw/novaseq_A01742
   
   multiqc_paths:
     - /data/fastq/

   logo:
     - ./assets/your_logo.png

   sequencers:
     - miseq1_M00818
     - miseq2_M04404
     - nextseq_NB501289
     - novaseq_A01742
   ```

   Ensure the logo path and sequencer names in the configuration match your setup.

## Deployment

### Setting Up the Environment

1. **Create a Conda Environment:**

   Create and activate a new conda environment:

   ```bash
   conda create -n seqmon python=3.11
   conda activate seqmon
   ```

2. **Install Dependencies:**

   Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To deploy Seqmon, run the following command:

```bash
python src/app.py
```

By default, the app will be served at `http://0.0.0.0:8050`.

## Feedback and Contributions

We welcome any feedback, suggestions, or contributions. Feel free to submit issues or pull requests on GitHub.