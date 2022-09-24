# MLops project

**This is study project for learning some ML technic elemets.**

### About project


### Repo structure:
#### (cookiecutter style)
- **data**
   - **external**    - up-to-date data
   - **interim**     - intermediate data that has been transformed
     - **cleaned**   - cleaned data after merging
     - **filtered**  - filtered data by station code
     - **updated**   - merged data historical with current
   - **processed**   - the final, canonical data sets for modeling
   - **raw**         - historical data from http://discomap.eea.europa.eu/  
- **metadata**   - meta information for scripts
- **models**     - trained and serialized models, model predictions, or model summaries
- **notebooks**  - jupyter notebooks
- **references** - paper for research
- **reports**    - generated analysis
- **src**        - source code for use in this project
  - **app** - script for model service with fastapi
  - **data**     - scripts to download or generate data
  - **features** - scripts to turn raw data into features for modeling
  - **models**   - scripts to train models and then use trained models to make predictions

Any information about docker containers, model service or experiments you can find in Wiki.

### How to use for experiments:
1. After creation venv istall all libraries
```commandline
poetry install
```
2. If not conda than run
```commandline
poetry shell
```
3. Run pipeline
```commandline
dvc repro
```
For one stage
```dvc repro <stage name>```
When you run pipeline for the first time there are no updated data, so merge will be passed.
4. To load updated data run script *data_loading_updated.py* by terminal command
```python data_loading_updated.py```
or via IDE.
If you run two functions in one day then updated data will be the same historical data.
All data is saved in *data/raw*.
Merged dataframes are saved into *data/interim*.

If you want to change any script, install pre-commit 
```
pre-commit install
```

