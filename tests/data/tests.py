import pandera as pa

from pandera import Column, DataFrameSchema, Index, Check

schema = DataFrameSchema(
    columns={
        'Countrycode': Column(str),
        'Namespace': Column(str),
        'AirQualityNetwork': Column(str),
        'AirQualityStationEoICode': Column(str),
        'SamplingPoint': Column(str),
        'SamplingProcess': Column(str),
        'Sample': Column(str),
        'AirPollutant': Column(str),
        'AirPollutantCode': Column(str),
        'AveragingTime': Column(str),
        'Concentration': Column(float),
        'UnitOfMeasurement': Column(str),
        'DatetimeBegin': Column(str),
        'DatetimeEnd': Column(str),
        'Validity': Column(int),
        'Verification': Column(int)
    },
    index=Index(
        str,
        Check(lambda x: x in ['Countrycode', 'Namespace', 'AirQualityNetwork', 'AirQualityStationEoICode',
                              'SamplingPoint', 'SamplingProcess', 'Sample', 'AirPollutant', 'AirPollutantCode',
                              'AveragingTime', 'Concentration', 'UnitOfMeasurement', 'DatetimeBegin', 'DatetimeEnd',
                              'Validity', 'Verification'])
    )
)