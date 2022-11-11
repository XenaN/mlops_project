# AQI prediction

**This is study project for learning some ML technic elemets.**

### Task
There are many pollutants in the air that worsen the quality of life of people. It's important to know about future air pollution. In this case we will find the best model to forecast it. For predicting we can monitor some pollutants or all. Here we choose to use Air Quality Index instead of several pollutants. If you want you can read the article from references to understand which diseases are connected with one or another pollutant.

Some points which you should know:
For calculation AQI we use ozone, SO2, NO2, CO, and PM10, PM2.5. The last ones are airborne particulate matter (PM). Those with a diameter of 10 microns or less (PM10) are inhalable into the lungs and can induce adverse health effects. Fine particulate matter is defined as particles that are 2.5 microns or less in diameter (PM2.5). Therefore, PM2.5 comprises a portion of PM10.

### Structure

So what do we do? We use api from discomap.eea.europa.eu to get some historical data, and also to get up-to-date data to forecast AQI. 
In metadata are saved configurations, where there are country, station, pollutant, and period for getting requests from api. 
Now discomap changed data structure, so you can download data from [link](https://drive.google.com/file/d/1wszz5UflHTDC9qGI7CdD5DGPFTmd1E9a/view?usp=share_link) and put it in *data/raw*.

DVC run pipeline with 
- data filtering by station
- merging with new data if needed
- cleaning data
- calculation AQI
- train model
- evaluate

**Pipeline**

![image](https://user-images.githubusercontent.com/43779450/201072233-0176f5fa-ddd3-4d5c-9b78-c5256bb8e6fb.png)


Research experiments you can read in notebooks/AQI_analysis.ipynb

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
- **references** - paper for research
- **reports**    - generated analysis
- **src**        - source code for use in this project
  - **app** - script for model service with fastapi
  - **data**     - scripts to download or generate data
  - **features** - scripts to turn raw data into features for modeling
  - **models**   - scripts to train models and then use trained models to make predictions

Any information about docker containers, model service or experiments you can find in Wiki.

### How to use:
#### Full way (if you want to reproduce whole pipeline) 
1. Download data (about 9 Gb unziped) from [link](https://drive.google.com/file/d/1wszz5UflHTDC9qGI7CdD5DGPFTmd1E9a/view?usp=share_link) and put it in *data/raw*.
2. After creation venv istall all libraries
```commandline
poetry install
```
3. If not conda than run
```commandline
poetry shell
```
4. Run pipeline
```commandline
dvc repro
```
5. Run
```
python service/main.py
```
6. Go to http://127.0.0.1:8000/ and look at statistics and prediction.

#### Easy way to run
1. Install several libs
```
pip install service/requirements.txt
```
2. Run
```
python service/main.py
```
3. Go to http://127.0.0.1:8000/ and look at statistics and prediction. Because there is saved model in repo.

Here you will see previous data and prediction for next day.

### Experiments
This is old project. Base models was tested some time ago.  Now we added CatBoost and some DL model.
Two widely used error measures are Mean Squared Error (MSE), and Root Mean Square Error (RMSE). These two measures give greater weight to large errors than to small ones. To overcome this problem, another widely used measure is the Mean Absolute Error (MAE). So we used both. 

The tabels below present best models. In notebooks there are many experiments with number of layers, learning rate and other parameters (it depends on model). 

**For one day prediction**

| Model | Features | How much days is used before | RMSE | MAE |
|-------|----------|------------------------------|------|-----|
|Naive (baseline)| AQI | One day| 13.8 | 7.7 |
| SARIMAX | AQI | All train data | 12.8 | 7.4 |
| RandomForest | Pollutants|  5 days | 13.8 | 8.4 |
| SVR | Pollutants | 5 days | 12.7 | 6.9 |
| XGBRegressor | Pollutants | 5 days | 10.9 | 6.8 |
| CatBoostRegressor | Pollutants | 5 days | 13.1 | 7.8 |
| LSTM (keras, custom architecture) | AQI | All train data | 12.2 | 7.2 |
| PyTorch Forecasting | AQI | All train data | 16.3 | 11.4 |
| FEDOT | AQI + PM2.5 | All train data | 15.7 | 9.8 |

As we can see best model for one day prediction is XGBoost. 
In our experiment for whole test set FEDOT make prediction with very low errors: RMSE - 6.4, 5.1. But for one day, it's very high.

**For 5 days prediction:**

| Model | Features | How much days is used before | RMSE | MAE |
|-------|----------|------------------------------|------|-----|
| SARIMAX | AQI | All train data | 18.7 | 11.5 |
| PyTorch Forecasting | AQI | All train data | 16.4 | 11.5 |
| FEDOT | AQI + PM2.5 | All train data | 18.2 | 11.7 |

For several day results are not very good, RMSE is about or more than std for AQI.

### Speed
On Macbook Air M1 8 cores RAM 8gb. Time - 1e-4. Std - 2e-5

![image](https://user-images.githubusercontent.com/43779450/201076989-02c1a719-364f-47a8-b974-466e6546dc0a.png)



### Code style
We use CI to check code style. There are several checks:

   * black
   * flack8

Tests work local.
