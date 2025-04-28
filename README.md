# VVIRAL

The primary functions of this repository include:

*   **Data Preprocessing**: Parsing raw AKTA result files (including `.res`, `.zip`, `.csv`, and `.xlsx` formats) to extract relevant experimental parameters and chromatogram data.
*   **Feature Engineering**: Transforming the extracted data into structured feature sets suitable for machine learning, including calculating peak metrics and collating run information.
*   **Predictive Modeling**: Building and training machine learning models to predict purification outcomes (e.g., "Total Capsids") based on process parameters.
*   **Bayesian Optimization**: Utilizing the trained model a surrogate within the BayBE framework to intelligently recommend new experimental conditions aimed at optimizing purification yield and purity.

## Environemnt Setup

`$ conda env create --name viral --file=viral.yml`

`$ conda activate viral`

## Project Structure

### `data_extraction`

This folder contains scripts used to parse and extract relevant data from historical chromatography runs, primarily from AKTA systems. Key scripts include:

*   `extract_matrix.py`: Extracts features from `.csv` files (likely exported from AKTA results).
*   `extract_xlsx_data.py`: Extracts features from `.xlsx` files.
*   `extract_peaks.py` & `extract_xlsx_peaks.py`: Extract peak-specific metrics from `.csv` and `.xlsx` files respectively.
*   `pycorn-bin.py`: A utility (likely based on the PyCORN library) used for processing AKTA `.res` or `.zip` result files, potentially converting them to `.xlsx` or `.csv`. See `extract_zips.sh` for usage example.
*   `utils.py` & `utils_xlsx.py`: Contain helper functions for data loading, parsing filenames (e.g., [`get_resin_and_serotype`](data_extraction/utils_xlsx.py), [`get_column_volume`](data_extraction/utils_xlsx.py)), calculating metrics, and potentially plotting ([`show_peaks`](data_extraction/utils_xlsx.py)).

The goal of these scripts is to generate structured datasets suitable for machine learning.

### `Modeling`

This folder contains scripts for building predictive models based on the data extracted in the `data_extraction` phase.

*   `train.py`: Script to train models (specifically Gaussian Process models as indicated). It loads processed data, splits it, potentially scales features ([`log_transform`](Modeling/utils.py)), trains a model ([`train_gp_model`](Modeling/models.py)), makes predictions ([`gp_predict`](Modeling/models.py)), and evaluates performance ([`get_metrics`](Modeling/utils.py)).
*   `models.py`: Likely defines the model architectures and training/prediction functions (e.g., Gaussian Process related functions).
*   `utils.py`: Contains helper functions for modeling, such as transformations ([`log_transform`](Modeling/utils.py), [`inverse_log_transform`](/Modeling/utils.py)) and metric calculation ([`get_metrics`](Modeling/utils.py)).
*   `ML_analysis.ipynb`: A Jupyter Notebook for exploratory data analysis and potentially model experimentation.

### `Optimization campaigns`

This folder contains scripts related to using the trained models for Bayesian optimization campaigns to suggest new experimental conditions.

*   `surrogate_model.py`: Defines the Gaussian Process surrogate model ([`gp_model`](Optimization%20campaigns/surrogate_model.py)) used within the optimization framework (BayBE). It specifies the kernel structure (using `DotProductKernel`, `RQKernel`, `MaternKernel`).
*   Each folder contains the serotypes that were purified in the downstream optimization campaign (AAV2, AAV5, AAV9).

## Workflow

1.  **Data Extraction**: Raw AKTA result files (e.g., `.res`, `.zip`) are processed using scripts in `data_extraction` (using `pycorn-bin.py` via `extract_zips.sh`) to generate intermediate `.csv` or `.xlsx` files.
2.  **Feature Engineering**: `extract_matrix.py`, `extract_xlsx_data.py`, and `extract_peaks.py` parse these intermediate files to create feature matrices and target variable datasets.
3.  **Model Training**: The `Modeling/train.py` script uses the generated datasets to train models.
4.  **Optimization**: The Gaussian process model (`surrogate_model.py`) is used as a surrogate in `Optimization campaigns` scripts (e.g., `AAV2_AAVA3_campaign.py`) to recommend new experimental conditions expected to optimize the target ("Total Capsids").

