# MLops project

### How to use:
1. After creation venv istall all libraries
```commandline
poetry install
```
2. Run script *data_loading.py*. For now use terminal or pycharm configuration. 
After ``if __name__ == "__main__"`` you can change input data according to *metadata/download_config.json*.
If you run two functions in one day than updated data will be the same historical.
All data is saved in *data/raw*.
3. Run *data_raw_merge.py* to concatenate historical and updated data. Merged dataframes are saved into *data/interim*.


### Repo structure:
#### (cookiecutter style)
- **data**
   - **external**    - data from third party sources
   - **interim**     - intermediate data that has been transformed
   - **processed**   - the final, canonical data sets for modeling
   - **raw**         - the original, immutable data dump
     - **historical_data_eea** - historical data from http://discomap.eea.europa.eu/
     - **updated_data_eea**    - up-to-date data from http://discomap.eea.europa.eu/
- **metadata**   - meta information for scripts
- **models**     - trained and serialized models, model predictions, or model summaries
- **notebooks**  - jupyter notebooks
- **reports**    - generated analysis
- **src**        - source code for use in this project
  - **data**     - scripts to download or generate data
  - **features** - scripts to turn raw data into features for modeling
  - **models**   - scripts to train models and then use trained models to make predictions
  - **visualisation** - scripts to create exploratory and results oriented visualizations


Authors: XenaN, Yaromir-hmel, inbfor