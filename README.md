# MLops project

**This is study project for learning some ML technic elemets.**

### About project
There are many pollutants in the air that worsen the quality of life of people. We can monitor some of them or all. In this case, we choose to use Air Quality Index instead of several pollutants. If you want you can read the article from references to understand which diseases are connected with one or another pollutant.

Some points which you should know:
For calculation AQI we use ozone, SO2, NO2, CO, and PM10, PM2.5. The last ones are airborne particulate matter (PM). Those with a diameter of 10 microns or less (PM10) are inhalable into the lungs and can induce adverse health effects. Fine particulate matter is defined as particles that are 2.5 microns or less in diameter (PM2.5). Therefore, PM2.5 comprises a portion of PM10.

### Structure

So what do we do? We use api from discomap.eea.europa.eu to get some historical data, and also to get up-to-date data to forecast AQI. 
In metadata are saved configurations, where there are country, station, pollutant, and period for getting requests from api. 

DVC run pipeline with 
- loading historical data
- filtering by station
- merging with new data if needed
- cleaning data
- calculation AQI
- train model
- evaluate

### How to use:
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


### Repo structure:
#### (cookiecutter style)
- **data**
   - **external**    - up-to-date data from http://discomap.eea.europa.eu/
   - **interim**     - intermediate data that has been transformed
     - **cleaned**   - cleaned data after merging
     - **filtered**  - filtered data by station code
     - **updated**   - merged data historical with current
   - **processed**   - the final, canonical data sets for modeling
   - **raw**         - historical data from http://discomap.eea.europa.eu/  
- **metadata**   - meta information for scripts
- **models**     - trained and serialized models, model predictions, or model summaries
- **notebooks**  - jupyter notebooks
- **reports**    - generated analysis
- **src**        - source code for use in this project
  - **data**     - scripts to download or generate data
  - **features** - scripts to turn raw data into features for modeling
  - **models**   - scripts to train models and then use trained models to make predictions
  - **visualisation** - scripts to create exploratory and results oriented visualizations
