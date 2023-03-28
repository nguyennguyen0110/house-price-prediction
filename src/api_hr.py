from flask import Flask, request, g

import json
import time
import datetime

import traceback
import math

import pandas as pd
import numpy as np
import joblib

# import os
# import hr_process
# import sys
# from common import utils

def initRouteWithPrefix(route_function, prefix='', mask='{0}{1}'):
    '''
      Defines a new route function with a prefix.
      The mask argument is a `format string` formatted with, in that order:
        prefix, route
    '''

    def newroute(route, *args, **kwargs):
        '''New function to prefix the route'''
        return route_function(mask.format(prefix, route), *args, **kwargs)

    return newroute


app = Flask(__name__)

require_fields = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'ExterQual', 'BsmtQual', 'KitchenQual', '1stFlrSF',
                  'GarageArea', 'YearBuilt', 'MSSubClass', 'GarageFinish', 'FullBath', 'LotFrontage', '2ndFlrSF', 'LotArea',
                  'TotRmsAbvGrd', 'YearRemodAdd', 'BsmtFinSF1', 'HeatingQC', 'Fireplaces', 'OpenPorchSF', 'BsmtUnfSF',
                  'OverallCond', 'MasVnrArea', 'HalfBath', 'BsmtExposure', 'GarageCond', 'WoodDeckSF', 'GarageQual',
                  'CentralAir', 'BedroomAbvGr', 'BsmtCond', 'PavedDrive', 'KitchenAbvGr', 'BsmtFullBath', 'ExterCond',
                  'ScreenPorch', 'EnclosedPorch', 'BsmtHalfBath',
                  'Neighborhood', 'GarageType', 'Foundation', 'Exterior2nd', 'BsmtFinType1', 'Exterior1st', 'MSZoning',
                  'MasVnrType', 'LotShape', 'HouseStyle', 'SaleType', 'SaleCondition', 'Electrical', 'BldgType',
                  'BsmtFinType2', 'LandContour', 'Condition1', 'Heating', 'RoofStyle', 'LotConfig']
valid_data_category = {
    "Neighborhood": ['Blmngtn', 'Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor', 'Edwards', 'Gilbert',
                     'IDOTRR', 'MeadowV', 'Mitchel', 'NAmes', 'NPkVill', 'NWAmes', 'NoRidge', 'NridgHt', 'OldTown', 'SWISU',
                     'Sawyer', 'SawyerW', 'Somerst', 'StoneBr', 'Timber', 'Veenker'],
    "GarageType": ['2Types', 'Attchd', 'Basment', 'BuiltIn', 'CarPort', 'Detchd', 'No_gara'],
    "Foundation": ['BrkTil', 'CBlock', 'PConc', 'Slab', 'Stone', 'Wood'],
    "Exterior2nd": ['AsbShng', 'AsphShn', 'Brk Cmn', 'BrkFace', 'CBlock', 'CmentBd', 'HdBoard', 'ImStucc', 'MetalSd', 'Other',
                    'Plywood', 'Stone', 'Stucco', 'VinylSd', 'Wd Sdng', 'Wd Shng'],
    "BsmtFinType1": ['ALQ', 'BLQ', 'GLQ', 'LwQ', 'No_bsmt', 'Rec', 'Unf'],
    "Exterior1st": ['AsbShng', 'AsphShn', 'BrkComm', 'BrkFace', 'CBlock', 'CemntBd', 'HdBoard', 'ImStucc', 'MetalSd',
                    'Plywood', 'Stone', 'Stucco', 'VinylSd', 'Wd Sdng', 'WdShing'],
    "MSZoning": ['C (all)', 'FV', 'RH', 'RL', 'RM'],
    "MasVnrType": ['BrkCmn', 'BrkFace', 'None', 'Stone'],
    "LotShape": ['IR1', 'IR2', 'IR3', 'Reg'],
    "HouseStyle": ['1.5Fin', '1.5Unf', '1Story', '2.5Fin', '2.5Unf', '2Story', 'SFoyer', 'SLvl'],
    "SaleType": ['COD', 'CWD', 'Con', 'ConLD', 'ConLI', 'ConLw', 'New', 'Oth', 'WD'],
    "SaleCondition": ['Abnorml', 'AdjLand', 'Alloca', 'Family', 'Normal', 'Partial'],
    "Electrical": ['FuseA', 'FuseF', 'FuseP', 'Mix', 'None', 'SBrkr'],
    "BldgType": ['1Fam', '2fmCon', 'Duplex', 'Twnhs', 'TwnhsE'],
    "BsmtFinType2": ['ALQ', 'BLQ', 'GLQ', 'LwQ', 'No_bsmt', 'Rec', 'Unf'],
    "LandContour": ['Bnk', 'HLS', 'Low', 'Lvl'],
    "Condition1": ['Artery', 'Feedr', 'Norm', 'PosA', 'PosN', 'RRAe', 'RRAn', 'RRNe', 'RRNn'],
    "Heating": ['Floor', 'GasA', 'GasW', 'Grav', 'OthW', 'Wall'],
    "RoofStyle": ['Flat', 'Gable', 'Gambrel', 'Hip', 'Mansard', 'Shed'],
    "LotConfig": ['Corner', 'CulDSac', 'FR2', 'FR3', 'Inside']
    }
valid_data_numerical = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'ExterQual', 'BsmtQual', 'KitchenQual',
                        '1stFlrSF', 'GarageArea', 'YearBuilt', 'MSSubClass', 'GarageFinish', 'FullBath', 'LotFrontage',
                        '2ndFlrSF', 'LotArea', 'TotRmsAbvGrd', 'YearRemodAdd', 'BsmtFinSF1', 'HeatingQC', 'Fireplaces',
                        'OpenPorchSF', 'BsmtUnfSF', 'OverallCond', 'MasVnrArea', 'HalfBath', 'BsmtExposure', 'GarageCond',
                        'WoodDeckSF', 'GarageQual', 'CentralAir', 'BedroomAbvGr', 'BsmtCond', 'PavedDrive', 'KitchenAbvGr',
                        'BsmtFullBath', 'ExterCond', 'ScreenPorch', 'EnclosedPorch', 'BsmtHalfBath']
one_hot_fields = ['Neighborhood_Blmngtn', 'Neighborhood_Blueste', 'Neighborhood_BrDale', 'Neighborhood_BrkSide',
                  'Neighborhood_ClearCr', 'Neighborhood_CollgCr', 'Neighborhood_Crawfor', 'Neighborhood_Edwards',
                  'Neighborhood_Gilbert', 'Neighborhood_IDOTRR', 'Neighborhood_MeadowV', 'Neighborhood_Mitchel',
                  'Neighborhood_NAmes', 'Neighborhood_NPkVill', 'Neighborhood_NWAmes', 'Neighborhood_NoRidge',
                  'Neighborhood_NridgHt', 'Neighborhood_OldTown', 'Neighborhood_SWISU', 'Neighborhood_Sawyer',
                  'Neighborhood_SawyerW', 'Neighborhood_Somerst', 'Neighborhood_StoneBr', 'Neighborhood_Timber',
                  'Neighborhood_Veenker',
                  'GarageType_2Types', 'GarageType_Attchd', 'GarageType_Basment', 'GarageType_BuiltIn', 'GarageType_CarPort',
                  'GarageType_Detchd', 'GarageType_No_gara',
                  'Foundation_BrkTil', 'Foundation_CBlock', 'Foundation_PConc', 'Foundation_Slab', 'Foundation_Stone',
                  'Foundation_Wood',
                  'Exterior2nd_AsbShng', 'Exterior2nd_AsphShn', 'Exterior2nd_Brk Cmn', 'Exterior2nd_BrkFace',
                  'Exterior2nd_CBlock', 'Exterior2nd_CmentBd', 'Exterior2nd_HdBoard', 'Exterior2nd_ImStucc',
                  'Exterior2nd_MetalSd', 'Exterior2nd_Other', 'Exterior2nd_Plywood', 'Exterior2nd_Stone', 'Exterior2nd_Stucco',
                  'Exterior2nd_VinylSd', 'Exterior2nd_Wd Sdng', 'Exterior2nd_Wd Shng',
                  'BsmtFinType1_ALQ', 'BsmtFinType1_BLQ', 'BsmtFinType1_GLQ', 'BsmtFinType1_LwQ', 'BsmtFinType1_No_bsmt',
                  'BsmtFinType1_Rec', 'BsmtFinType1_Unf',
                  'Exterior1st_AsbShng', 'Exterior1st_AsphShn', 'Exterior1st_BrkComm', 'Exterior1st_BrkFace',
                  'Exterior1st_CBlock', 'Exterior1st_CemntBd', 'Exterior1st_HdBoard', 'Exterior1st_ImStucc',
                  'Exterior1st_MetalSd', 'Exterior1st_Plywood', 'Exterior1st_Stone', 'Exterior1st_Stucco',
                  'Exterior1st_VinylSd', 'Exterior1st_Wd Sdng', 'Exterior1st_WdShing',
                  'MSZoning_C (all)', 'MSZoning_FV', 'MSZoning_RH', 'MSZoning_RL', 'MSZoning_RM',
                  'MasVnrType_BrkCmn', 'MasVnrType_BrkFace', 'MasVnrType_None', 'MasVnrType_Stone',
                  'LotShape_IR1', 'LotShape_IR2', 'LotShape_IR3', 'LotShape_Reg',
                  'HouseStyle_1.5Fin', 'HouseStyle_1.5Unf', 'HouseStyle_1Story', 'HouseStyle_2.5Fin', 'HouseStyle_2.5Unf',
                  'HouseStyle_2Story', 'HouseStyle_SFoyer', 'HouseStyle_SLvl',
                  'SaleType_COD', 'SaleType_CWD', 'SaleType_Con', 'SaleType_ConLD', 'SaleType_ConLI', 'SaleType_ConLw',
                  'SaleType_New', 'SaleType_Oth', 'SaleType_WD',
                  'SaleCondition_Abnorml', 'SaleCondition_AdjLand', 'SaleCondition_Alloca', 'SaleCondition_Family',
                  'SaleCondition_Normal', 'SaleCondition_Partial',
                  'Electrical_FuseA', 'Electrical_FuseF', 'Electrical_FuseP', 'Electrical_Mix', 'Electrical_None',
                  'Electrical_SBrkr',
                  'BldgType_1Fam', 'BldgType_2fmCon', 'BldgType_Duplex', 'BldgType_Twnhs', 'BldgType_TwnhsE',
                  'BsmtFinType2_ALQ', 'BsmtFinType2_BLQ', 'BsmtFinType2_GLQ', 'BsmtFinType2_LwQ', 'BsmtFinType2_No_bsmt',
                  'BsmtFinType2_Rec', 'BsmtFinType2_Unf',
                  'LandContour_Bnk', 'LandContour_HLS', 'LandContour_Low', 'LandContour_Lvl',
                  'Condition1_Artery', 'Condition1_Feedr', 'Condition1_Norm', 'Condition1_PosA', 'Condition1_PosN',
                  'Condition1_RRAe', 'Condition1_RRAn', 'Condition1_RRNe', 'Condition1_RRNn',
                  'Heating_Floor', 'Heating_GasA', 'Heating_GasW', 'Heating_Grav', 'Heating_OthW', 'Heating_Wall',
                  'RoofStyle_Flat', 'RoofStyle_Gable', 'RoofStyle_Gambrel', 'RoofStyle_Hip', 'RoofStyle_Mansard',
                  'RoofStyle_Shed',
                  'LotConfig_Corner', 'LotConfig_CulDSac', 'LotConfig_FR2', 'LotConfig_FR3', 'LotConfig_Inside']
numerical_columns = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'ExterQual', 'BsmtQual', 'KitchenQual',
                     '1stFlrSF', 'GarageArea', 'HouseAge', 'MSSubClass', 'GarageFinish', 'FullBath', 'LotFrontage', '2ndFlrSF',
                     'LotArea', 'TotRmsAbvGrd', 'RemodelAge', 'BsmtFinSF1', 'HeatingQC', 'Fireplaces', 'OpenPorchSF',
                     'BsmtUnfSF', 'OverallCond', 'MasVnrArea', 'HalfBath', 'BsmtExposure', 'GarageCond', 'WoodDeckSF',
                     'GarageQual', 'CentralAir', 'BedroomAbvGr', 'BsmtCond', 'PavedDrive', 'KitchenAbvGr', 'BsmtFullBath',
                     'ExterCond', 'ScreenPorch', 'EnclosedPorch', 'BsmtHalfBath']
category_columns = ['Neighborhood', 'GarageType', 'Foundation', 'Exterior2nd', 'BsmtFinType1', 'Exterior1st', 'MSZoning',
                    'MasVnrType', 'LotShape', 'HouseStyle', 'SaleType', 'SaleCondition', 'Electrical', 'BldgType',
                    'BsmtFinType2', 'LandContour', 'Condition1', 'Heating', 'RoofStyle', 'LotConfig']
columns = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'ExterQual', 'BsmtQual', 'KitchenQual', '1stFlrSF',
           'GarageArea', 'HouseAge', 'MSSubClass', 'GarageFinish', 'FullBath', 'LotFrontage', '2ndFlrSF', 'LotArea',
           'TotRmsAbvGrd', 'RemodelAge', 'BsmtFinSF1', 'HeatingQC', 'Fireplaces', 'OpenPorchSF', 'BsmtUnfSF', 'OverallCond',
           'MasVnrArea', 'HalfBath', 'BsmtExposure', 'GarageCond', 'WoodDeckSF', 'GarageQual', 'CentralAir', 'BedroomAbvGr',
           'BsmtCond', 'PavedDrive', 'KitchenAbvGr', 'BsmtFullBath', 'ExterCond', 'ScreenPorch', 'EnclosedPorch',
           'BsmtHalfBath',
           'Neighborhood_Blmngtn', 'Neighborhood_Blueste', 'Neighborhood_BrDale', 'Neighborhood_BrkSide',
           'Neighborhood_ClearCr', 'Neighborhood_CollgCr', 'Neighborhood_Crawfor', 'Neighborhood_Edwards',
           'Neighborhood_Gilbert', 'Neighborhood_IDOTRR', 'Neighborhood_MeadowV', 'Neighborhood_Mitchel', 'Neighborhood_NAmes',
           'Neighborhood_NPkVill', 'Neighborhood_NWAmes', 'Neighborhood_NoRidge', 'Neighborhood_NridgHt',
           'Neighborhood_OldTown', 'Neighborhood_SWISU', 'Neighborhood_Sawyer', 'Neighborhood_SawyerW', 'Neighborhood_Somerst',
           'Neighborhood_StoneBr', 'Neighborhood_Timber', 'Neighborhood_Veenker',
           'GarageType_2Types', 'GarageType_Attchd', 'GarageType_Basment', 'GarageType_BuiltIn', 'GarageType_CarPort',
           'GarageType_Detchd', 'GarageType_No_gara',
           'Foundation_BrkTil', 'Foundation_CBlock', 'Foundation_PConc', 'Foundation_Slab', 'Foundation_Stone',
           'Foundation_Wood',
           'Exterior2nd_AsbShng', 'Exterior2nd_AsphShn', 'Exterior2nd_Brk Cmn', 'Exterior2nd_BrkFace', 'Exterior2nd_CBlock',
           'Exterior2nd_CmentBd', 'Exterior2nd_HdBoard', 'Exterior2nd_ImStucc', 'Exterior2nd_MetalSd', 'Exterior2nd_Other',
           'Exterior2nd_Plywood', 'Exterior2nd_Stone', 'Exterior2nd_Stucco', 'Exterior2nd_VinylSd', 'Exterior2nd_Wd Sdng',
           'Exterior2nd_Wd Shng',
           'BsmtFinType1_ALQ', 'BsmtFinType1_BLQ', 'BsmtFinType1_GLQ', 'BsmtFinType1_LwQ', 'BsmtFinType1_No_bsmt',
           'BsmtFinType1_Rec', 'BsmtFinType1_Unf',
           'Exterior1st_AsbShng', 'Exterior1st_AsphShn', 'Exterior1st_BrkComm', 'Exterior1st_BrkFace', 'Exterior1st_CBlock',
           'Exterior1st_CemntBd', 'Exterior1st_HdBoard', 'Exterior1st_ImStucc', 'Exterior1st_MetalSd', 'Exterior1st_Plywood',
           'Exterior1st_Stone', 'Exterior1st_Stucco', 'Exterior1st_VinylSd', 'Exterior1st_Wd Sdng', 'Exterior1st_WdShing',
           'MSZoning_C (all)', 'MSZoning_FV', 'MSZoning_RH', 'MSZoning_RL', 'MSZoning_RM',
           'MasVnrType_BrkCmn', 'MasVnrType_BrkFace', 'MasVnrType_None', 'MasVnrType_Stone',
           'LotShape_IR1', 'LotShape_IR2', 'LotShape_IR3', 'LotShape_Reg',
           'HouseStyle_1.5Fin', 'HouseStyle_1.5Unf', 'HouseStyle_1Story', 'HouseStyle_2.5Fin', 'HouseStyle_2.5Unf',
           'HouseStyle_2Story', 'HouseStyle_SFoyer', 'HouseStyle_SLvl',
           'SaleType_COD', 'SaleType_CWD', 'SaleType_Con', 'SaleType_ConLD', 'SaleType_ConLI', 'SaleType_ConLw',
           'SaleType_New', 'SaleType_Oth', 'SaleType_WD',
           'SaleCondition_Abnorml', 'SaleCondition_AdjLand', 'SaleCondition_Alloca', 'SaleCondition_Family',
           'SaleCondition_Normal', 'SaleCondition_Partial',
           'Electrical_FuseA', 'Electrical_FuseF', 'Electrical_FuseP', 'Electrical_Mix', 'Electrical_None', 'Electrical_SBrkr',
           'BldgType_1Fam', 'BldgType_2fmCon', 'BldgType_Duplex', 'BldgType_Twnhs', 'BldgType_TwnhsE',
           'BsmtFinType2_ALQ', 'BsmtFinType2_BLQ', 'BsmtFinType2_GLQ', 'BsmtFinType2_LwQ', 'BsmtFinType2_No_bsmt',
           'BsmtFinType2_Rec', 'BsmtFinType2_Unf',
           'LandContour_Bnk', 'LandContour_HLS', 'LandContour_Low', 'LandContour_Lvl',
           'Condition1_Artery', 'Condition1_Feedr', 'Condition1_Norm', 'Condition1_PosA', 'Condition1_PosN', 'Condition1_RRAe',
           'Condition1_RRAn', 'Condition1_RRNe', 'Condition1_RRNn',
           'Heating_Floor', 'Heating_GasA', 'Heating_GasW', 'Heating_Grav', 'Heating_OthW', 'Heating_Wall',
           'RoofStyle_Flat', 'RoofStyle_Gable', 'RoofStyle_Gambrel', 'RoofStyle_Hip', 'RoofStyle_Mansard', 'RoofStyle_Shed',
           'LotConfig_Corner', 'LotConfig_CulDSac', 'LotConfig_FR2', 'LotConfig_FR3', 'LotConfig_Inside']
skewed_features = ['GrLivArea', 'ExterQual', '1stFlrSF', 'MSSubClass', '2ndFlrSF', 'LotArea', 'OpenPorchSF', 'BsmtUnfSF',
                   'MasVnrArea', 'BsmtExposure', 'WoodDeckSF', 'KitchenAbvGr', 'ExterCond', 'ScreenPorch', 'EnclosedPorch',
                   'BsmtHalfBath']
ensemble_model = None
scaler = joblib.load(filename="models/scaler.joblib")

@app.before_request
def before_request():
    g.request_start_time = time.time()


@app.teardown_request
def teardown_request(exception=None):
    print("From before_request to teardown_request: %.2fms" % ((time.time() - g.request_start_time) * 1000))


@app.route("/", defaults={"path": ""}, methods=['GET', 'POST'])
@app.route("/<path:path>", methods=['GET', 'POST'])
def do_upload_file(path):
    if request.method == 'GET':
        return "hello, world"
    if request.method == 'POST':
        try:
            # utils.AppConfig.write_log(request, False)
            # config = request.get_json()
            # utils.AppConfig.write_log(config, False)

            ################################################
            #TODO: call your predictive function here
            
            # Get data from request body
            data = request.get_json()
            
            # Check if all require fields provided
            for field in require_fields:
                if not field in data.keys():
                    return "Must give enough information to predict house price. Check readme file for details."
            
            # Check valid value
            for key in valid_data_category.keys():
                if data[key] not in valid_data_category[key]:
                    return "Invalid value(s). Check readme file for details."
            
            for key in valid_data_numerical:
                if type(data[key]) != int and type(data[key]) != float:
                    return "Invalid value(s). Check readme file for details."
            
            # One-hot coding for category features
            for field in one_hot_fields:
                data[field] = 0
            for column in category_columns:
                data[f"{column}_{data[column]}"] = 1
            
            # Change data from dictionary to dataframe
            data = pd.DataFrame(data, index=[0])
            data = data.drop(columns=category_columns)
            
            # Turn "YearBuilt" & "YearRemodAdd" to "HouseAge" & "RemodelAge"
            today = datetime.date.today()
            this_year = today.year
            data["HouseAge"] = this_year - data["YearBuilt"]
            data["RemodelAge"] = this_year - data["YearRemodAdd"]
            data = data.drop(columns=["YearBuilt", "YearRemodAdd"])
            
            # Normalize skew features
            for f in skewed_features:
                data[f] = np.log1p(data[f])
            
            # Standardize numerical columns
            data[numerical_columns] = scaler.transform(data[numerical_columns])
            
            # Make sure our features in correct order
            data = data[columns]
            
            # Get predictions from our models
            ensemble_predict = ensemble_model.predict(data)
            
            ################################################
            
            #TODO: write your return the result here
            return f"The predicted price for this house is about {math.ceil(np.expm1(ensemble_predict)):,} USD"

        except Exception as inst:
            error = "Error:"
            traceback_str = ''.join(traceback.format_tb(inst.__traceback__))
            error += traceback_str
            # utils.AppConfig.write_log(traceback_str, True)
            # utils.AppConfig.write_log(inst, True)
            data = {
                'Status': error
            }
            return json.dumps(data, ensure_ascii=False)

if __name__ == '__main__':
    ensemble_model = joblib.load(filename="models/ensemble_model.joblib")
    print("*************************************************************")
    print("*************************************************************")
    print("************************ APP RUNNING ************************")
    print("*************************************************************")
    print("*************************************************************")
    app.run(debug=False, host='0.0.0.0', port=8099, threaded=True)
