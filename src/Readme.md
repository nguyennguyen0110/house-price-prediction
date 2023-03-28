# Hướng dẫn dùng API dự đoán giá nhà ở thành phố Ames, bang Iowa
- *Bạn có thể sẽ cần cài đặt flask để chạy server trên máy tính cá nhân*

      conda install -c conda-forge flask=2.2.2
- *File dữ liệu và mô tả trong folder "./data"*
- *Các files phân tích dữ liệu, xây dựng mô hình trong folder "./notebook"*
- *Các files báo cáo trong folder "./reports"*

Để chạy server, hãy mở file "./src/api_hr.py" bằng phần mềm Spyder (được cài đặt khi cài Anaconda Navigator) sau đó click "Run file(F5)". Hoặc bạn cũng có thể chạy server bằng lệnh flask trong command line "flask --app api_hr run".

Để dùng API, hãy dùng phần mềm Postman để gọi đến địa chỉ local server đang chạy:
    
    http://127.0.0.1:8099

- Phương thức GET: sẽ trả về dòng chữ *"hello, world"*
- Phương thức POST: bạn cần cung cấp thông tin về ngôi nhà để dự đoán giá trong request body. Nếu cung cấp đầy đủ thông tin với giá trị hợp lệ sẽ trả về dòng chữ "The predicted price for this house is about *xxx* USD", trong đó *xxx* là giá nhà dự đoán. Nếu không cung cấp đủ thông tin sẽ trả về *"Must give enough information to predict house price. Check readme file for details."*, nếu thông tin cung cấp giá trị không hợp lệ sẽ trả về *"Invalid value(s). Check readme file for details."*. 

      {
          "OverallQual": Đánh giá vật liệu tổng thể và hoàn thiện của ngôi nhà,
          "OverallCond": Đánh giá tình trạng chung của ngôi nhà,
          "ExterQual": Đánh giá chất lượng vật liệu bên ngoài,
          "BsmtQual": Đánh giá chiều cao của tầng hầm,
          "KitchenQual": Chất lượng nhà bếp,
          "HeatingQC": Chất lượng và điều kiện máy sưởi,
          "LotArea": Diện tích lô,
          "GrLivArea": Diện tích sinh hoạt (phía trên mặt đất),
          "TotalBsmtSF": Tổng diện tích tầng hầm,
          "1stFlrSF": Diện tích tầng 1,
          "2ndFlrSF": Diện tích tầng 2,
          "OpenPorchSF": Diện tích hiên nhà (mở),
          "MasVnrArea": Diện tích gạch ốp
          "WoodDeckSF": Diện tích sàn gỗ
          "GarageCars": Ga-ra chứa khoảng mấy chiêc xe hơi,
          "GarageArea": Diện tích ga-ra,
          "GarageFinish": Hoàn thiện nội thất ga-ra,
          "GarageCond": Tình trạng ga-ra,
          "GarageQual": Chất lượng ga-ra,
          "BsmtFinSF1": Diện tích khu vực hoàn thiện 1,
          "BsmtUnfSF": Diện tích tầng hầm chưa hoàn thành,
          "BsmtExposure": Mức thông thoáng của tầng hầm,
          "BsmtCond": Đánh giá tình trạng chung của tầng hầm,
          "BsmtFullBath": Tầng hầm đầy đủ phòng tắm,
          "BsmtHalfBath": Tầng hầm nửa số phòng tắm,
          "ExterCond": Đánh giá tình trạng hiện tại của vật liệu bên ngoài,
          "LotFrontage": Lề đường trước nhà,
          "YearBuilt": Năm xây dựng,
          "YearRemodAdd": Năm tu sửa,
          "FullBath": Đầy đủ nhà tắm phía trên mặt đất,
          "HalfBath": Nửa số nhà tắm phia trên mặt đất,
          "TotRmsAbvGrd": Tổng phòng phía trên (không tính nhà tắm),
          "BedroomAbvGr": Số phòng ngủ phía trên (không tính tầng hầm),
          "KitchenAbvGr": Số nhà bếp phía trên,
          "Fireplaces": Số lò sưởi (đốt bằng lửa),
          "MSSubClass": Loại nhà,
          "CentralAir": Máy điều hòa trung tâm,
          "PavedDrive": Đường xe ra có trải nhựa không,
          "ScreenPorch": Diện tích hiên có màn che (ngăn côn trùng, chắn bớt nắng, ...),
          "EnclosedPorch": Diện tích hiên nhà (vây kín),
          "Neighborhood": Vị trí (trong thành phố Ames, bang Iowa),
          "GarageType": Vị trí ga-ra,
          "Foundation": Loại móng nhà,
          "Exterior1st": Lớp phủ ngôi nhà,
          "Exterior2nd": Lớp phủ ngôi nhà (nếu nhà được phủ bởi 2 loại vật liệu),
          "BsmtFinType1": Đánh giá khu vực hoàn thiện tầng hầm 1,
          "BsmtFinType2": Đánh giá khu vực hoàn thiện tầng hầm loại 2,
          "MSZoning": Phân loại khu vực,
          "LandContour": Độ phẳng của lô đất,
          "MasVnrType": Loại gạch ốp (gạch, đá, gỗ, ...),
          "LotShape": Hình dạng lô đất,
          "HouseStyle": Phong cách xây dựng,
          "SaleType": Loại hợp đồng mua bán nhà,
          "SaleCondition": Loại hình (điều kiện) mua bán,
          "Electrical": Hệ thống điện,
          "BldgType": Loại nhà ở (nhà riêng 1 gia đình / 2 gia đình / nhà phố / ... ),
          "Condition1": Có ở gần tuyến đường huyết mạch, đường sắt, ... nào không,
          "Heating": Loại hình sưởi,
          "RoofStyle": Loại mái,
          "LotConfig": Thế đất (ngõ cụt, 2 mặt tiền, 3 mặt tiền, ...)
      }
Trong đó mỗi thông tin chỉ nhận một số giá trị nhất định:
- "OverallQual": số từ 1 - 10 tương ứng chất lượng từ rất kém đến rất tốt
- "OverallCond": số từ 1 - 10 tương ứng chất lượng từ rất kém đến rất tốt
- "ExterQual": số từ 1 - 5 tương ứng chất lượng từ rất kém đến rất tốt
- "BsmtQual": số từ 1 - 5 tương ứng chất lượng từ rất kém đến rất tốt, để 0 nếu không có tầng hầm
- "KitchenQual": số từ 1 - 5 tương ứng chất lượng từ rất kém đến rất tốt
- "HeatingQC": số từ 1 - 5 tương ứng chất lượng từ rất kém đến rất tốt
- "LotArea": số (ĐVT: square feet)
- "GrLivArea": số (ĐVT: square feet)
- "TotalBsmtSF": số (ĐVT: square feet, để 0 nếu không có tầng hầm)
- "1stFlrSF": số (ĐVT: square feet)
- "2ndFlrSF": số (ĐVT: square feet)
- "OpenPorchSF": số (ĐVT: square feet)
- "MasVnrArea": số (ĐVT: square feet)
- "WoodDeckSF": số (ĐVT: square feet)
- "GarageCars": số (ĐVT: chiếc, để giá trị 0 nếu không có ga-ra)
- "GarageArea": số (ĐVT: square feet, để giá trị 0 nếu không có ga-ra)
- "GarageFinish": số:
  - 0: No Garage
  - 1: Unfinished
  - 2: Rough Finished
  - 3: Finished
- "GarageCond": số từ 1 - 5 tương ứng chất lượng từ rất kém đến rất tốt, để 0 nếu không có ga-ra
- "GarageQual": số từ 1 - 5 tương ứng chất lượng từ rất kém đến rất tốt, để 0 nếu không có ga-ra
- "BsmtFinSF1": số (ĐVT: square feet)
- "BsmtUnfSF": số (ĐVT: square feet)
- "BsmtExposure": số từ 1 - 5 tương ứng chất lượng từ rất kém đến rất tốt, để 0 nếu không có tầng hầm
- "BsmtCond": số từ 1 - 5 tương ứng chất lượng từ rất kém đến rất tốt, để 0 nếu không có tầng hầm
- "BsmtFullBath": số (ĐVT: phòng)
- "BsmtHalfBath": số (ĐVT: phòng)
- "ExterCond": số từ 1 - 5 tương ứng chất lượng từ rất kém đến rất tốt
- "LotFrontage": số (ĐVT: feet)
- "YearBuilt": số (chỉ ghi năm ngôi nhà được xây)
- "YearRemodAdd": số (ghi năm ngôi nhà được tu sửa lần cuối, nếu chưa sửa gì thì để cùng năm xây dựng)
- "FullBath": số (ĐVT: cái)
- "HalfBath": số (ĐVT: cái)
- "TotRmsAbvGrd": số (ĐVT: phòng)
- "BedroomAbvGr": số (ĐVT: phòng)
- "KitchenAbvGr": số (ĐVT: phòng)
- "Fireplaces": số (ĐVT: cái)
- "MSSubClass": số
  - 20: 1-STORY 1946 & NEWER ALL STYLES
  - 30: 1-STORY 1945 & OLDER
  - 40: 1-STORY W/FINISHED ATTIC ALL AGES
  - 45: 1-1/2 STORY - UNFINISHED ALL AGES
  - 50: 1-1/2 STORY FINISHED ALL AGES
  - 60: 2-STORY 1946 & NEWER
  - 70: 2-STORY 1945 & OLDER
  - 75: 2-1/2 STORY ALL AGES
  - 80: SPLIT OR MULTI-LEVEL
  - 85: SPLIT FOYER
  - 90: DUPLEX - ALL STYLES AND AGES
  - 120: 1-STORY PUD (Planned Unit Development) - 1946 & NEWER
  - 150: 1-1/2 STORY PUD - ALL AGES
  - 160: 2-STORY PUD - 1946 & NEWER
  - 180: PUD - MULTILEVEL - INCL SPLIT LEV/FOYER
  - 190: 2 FAMILY CONVERSION - ALL STYLES AND AGES
- "CentralAir": số
  - 0: No
  - 1: Yes
- "PavedDrive": số
  - 0: Dirt/Gravel
  - 1: Partial Pavement
  - 2: Paved
- "ScreenPorch": số (ĐVT: square feet)
- "EnclosedPorch": số (ĐVT: square feet)
- "Neighborhood": chuỗi, chỉ nhận một trong các giá trị sau
  - "Blmngtn": Bloomington Heights
  - "Blueste": Bluestem
  - "BrDale": Briardale
  - "BrkSide": Brookside
  - "ClearCr": Clear Creek
  - "CollgCr": College Creek
  - "Crawfor": Crawford
  - "Edwards": Edwards
  - "Gilbert": Gilbert
  - "IDOTRR": Iowa DOT and Rail Road
  - "MeadowV": Meadow Village
  - "Mitchel": Mitchell
  - "NAmes": North Ames
  - "NPkVill": Northpark Villa
  - "NWAmes": Northwest Ames
  - "NoRidge": Northridge
  - "NridgHt": Northridge Heights
  - "OldTown": Old Town
  - "SWISU": South & West of Iowa State University
  - "Sawyer": Sawyer
  - "SawyerW": Sawyer West
  - "Somerst": Somerset
  - "StoneBr": Stone Brook
  - "Timber": Timberland
  - "Veenker": Veenker
- "GarageType": chuỗi, chỉ nhận một trong các giá trị sau
  - "2Types": More than one type of garage
  - "Attchd": Attached to home
  - "Basment": Basement Garage
  - "BuiltIn": Built-In (Garage part of house - typically has room above garage)
  - "CarPort": Car Port
  - "Detchd": Detached from home
  - "No_gara": No Garage
- "Foundation": chuỗi
  - "BrkTil": Brick & Tile
  - "CBlock": Cinder Block
  - "PConc": Poured Contrete
  - "Slab"
  - "Stone"
  - "Wood"
- "Exterior1st": chuỗi
  - "AsbShng": Asbestos Shingles
  - "AsphShn": Asphalt Shingles
  - "BrkComm": Brick Common
  - "BrkFace": Brick Face
  - "CBlock": Cinder Block
  - "CemntBd": Cement Board
  - "HdBoard": Hard Board
  - "ImStucc": Imitation Stucco
  - "MetalSd": Metal Siding
  - "Plywood": Plywood
  - "Stone": Stone
  - "Stucco": Stucco
  - "VinylSd": Vinyl Siding
  - "Wd Sdng": Wood Siding
  - "WdShing": Wood Shingles
- "Exterior2nd": chuỗi
  - "AsbShng": Asbestos Shingles
  - "AsphShn": Asphalt Shingles
  - "Brk Cmn": Brick Common
  - "BrkFace": Brick Face
  - "CBlock": Cinder Block
  - "CmentBd": Cement Board"
  - "HdBoard": Hard Board
  - "ImStucc": Imitation Stucco
  - "MetalSd": Metal Siding
  - "Other": Other
  - "Plywood": Plywood
  - "Stone": Stone
  - "Stucco": Stucco
  - "VinylSd": Vinyl Siding
  - "Wd Sdng": Wood Siding
  - "Wd Shng": Wood Shingles
- "BsmtFinType1": chuỗi
  - "GLQ": Good Living Quarters
  - "ALQ": Average Living Quarters
  - "BLQ": Below Average Living Quarters
  - "Rec": Average Rec Room
  - "LwQ": Low Quality
  - "Unf": Unfinshed
  - "No_bsmt": No basement
- "BsmtFinType2": chuỗi, chỉ nhận một trong các giá trị sau
  - "GLQ": Good Living Quarters
  - "ALQ": Average Living Quarters
  - "BLQ": Below Average Living Quarters
  - "Rec": Average Rec Room
  - "LwQ": Low Quality
  - "Unf": Unfinshed
  - "No_bsmt": No basement
- "MSZoning": chuỗi, chỉ nhận một trong các giá trị sau
  - "C (all)": Commercial
  - "FV": Floating Village Residential
  - "RH": Residential High Density
  - "RL": Residential Low Density
  - "RM": Residential Medium Density
- "LandContour": chuỗi, chỉ nhận một trong các giá trị sau
  - 'Bnk': Banked - Quick and significant rise from street grade to building
  - 'HLS': Hillside - Significant slope from side to side
  - 'Low': Depression
  - 'Lvl': Near Flat/Level
- "MasVnrType": chuỗi, chỉ nhận một trong các giá trị sau
  - 'BrkCmn': Brick Common
  - 'BrkFace': Brick Face
  - 'Stone'
  - 'None'
- "LotShape": chuỗi, chỉ nhận một trong các giá trị sau
  - 'IR1': Slightly irregular
  - 'IR2': Moderately Irregular
  - 'IR3': Irregular
  - 'Reg': Regular
- "HouseStyle": chuỗi, chỉ nhận một trong các giá trị sau
  - '1Story': One story
  - '1.5Fin': One and one-half story: 2nd level finished
  - '1.5Unf': One and one-half story: 2nd level unfinished
  - '2Story': Two story
  - '2.5Fin': Two and one-half story: 2nd level finished
  - '2.5Unf': Two and one-half story: 2nd level unfinished
  - 'SFoyer': Split Foyer
  - 'SLvl': Split Level
- "SaleType": chuỗi, chỉ nhận một trong các giá trị sau
  - 'COD': Court Officer Deed/Estate
  - 'CWD': Warranty Deed - Cash
  - 'Con': Contract 15% Down payment regular terms
  - 'ConLD': Contract Low Down
  - 'ConLI': Contract Low Interest
  - 'ConLw': Contract Low Down payment and low interest
  - 'New': Home just constructed and sold
  - 'Oth': Other
  - 'WD': Warranty Deed - Conventional
- "SaleCondition": chuỗi, chỉ nhận một trong các giá trị sau
  - 'Abnorml': Abnormal Sale -  trade, foreclosure, short sale
  - 'AdjLand': Adjoining Land Purchase
  - 'Alloca': Allocation - two linked properties with separate deeds, typically condo with a garage unit
  - 'Family': Sale between family members
  - 'Normal': Normal Sale
  - 'Partial': Home was not completed when last assessed (associated with New Homes)
- "Electrical": chuỗi, chỉ nhận một trong các giá trị sau
  - 'FuseA': Fuse Box over 60 AMP and all Romex wiring (Average)
  - 'FuseF': 60 AMP Fuse Box and mostly Romex wiring (Fair)
  - 'FuseP': 60 AMP Fuse Box and mostly knob & tube wiring (poor)
  - 'Mix': Mixed
  - 'SBrkr': Standard Circuit Breakers & Romex
  - 'None'
- "BldgType": chuỗi, chỉ nhận một trong các giá trị sau
  - '1Fam': Single-family Detached
  - '2fmCon': Two-family Conversion; originally built as one-family dwelling
  - 'Duplex': Duplex
  - 'Twnhs': Townhouse Inside Unit
  - 'TwnhsE': Townhouse End Unit
- "Condition1": chuỗi, chỉ nhận một trong các giá trị sau
  - 'Artery': Adjacent to arterial street
  - 'Feedr': Adjacent to feeder street
  - 'Norm': Normal
  - 'PosA': Adjacent to postive off-site feature
  - 'PosN': Near positive off-site feature--park, greenbelt, etc.
  - 'RRAe': Adjacent to East-West Railroad
  - 'RRAn': Adjacent to North-South Railroad
  - 'RRNe': Within 200' of East-West Railroad
  - 'RRNn': Within 200' of North-South Railroad
- "Heating": chuỗi, chỉ nhận một trong các giá trị sau
  - 'Floor': Floor Furnace
  - 'GasA': Gas forced warm air furnace
  - 'GasW': Gas hot water or steam heat
  - 'Grav': Gravity furnace
  - 'Wall': Wall furnace
  - 'OthW': Hot water or steam heat other than gas
- "RoofStyle": chuỗi, chỉ nhận một trong các giá trị sau
  - 'Flat'
  - 'Gable'
  - 'Gambrel': Gabrel (Barn)
  - 'Hip'
  - 'Mansard'
  - 'Shed'
- "LotConfig": chuỗi, chỉ nhận một trong các giá trị sau
  - 'Corner': Corner lot
  - 'CulDSac': Cul-de-sac
  - 'FR2': Frontage on 2 sides of property
  - 'FR3': Frontage on 3 sides of property
  - 'Inside': Inside lot

*Ví dụ về thông tin ngôi nhà cần được dự đoán giá:*

    {
        "OverallQual": 7,
        "OverallCond": 6,
        "ExterQual": 4,
        "BsmtQual": 4,
        "KitchenQual": 4,
        "HeatingQC": 5,
        "LotArea": 5000,
        "GrLivArea": 1750,
        "TotalBsmtSF": 1250,
        "1stFlrSF": 1350,
        "2ndFlrSF": 700,
        "OpenPorchSF": 100,
        "MasVnrArea": 400,
        "WoodDeckSF": 150,
        "GarageCars": 2,
        "GarageArea": 570,
        "GarageFinish": 3,
        "GarageCond": 4,
        "GarageQual": 4,
        "BsmtFinSF1": 700,
        "BsmtUnfSF": 200,
        "BsmtExposure": 4,
        "BsmtCond": 4,
        "BsmtFullBath": 1,
        "BsmtHalfBath": 0,
        "ExterCond": 4,
        "LotFrontage": 100,
        "YearBuilt": 2000,
        "YearRemodAdd": 2010,
        "FullBath": 2,
        "HalfBath": 1,
        "TotRmsAbvGrd": 7,
        "BedroomAbvGr": 2,
        "KitchenAbvGr": 1,
        "Fireplaces": 1,
        "MSSubClass": 50,
        "CentralAir": 1,
        "PavedDrive": 2,
        "ScreenPorch": 0,
        "EnclosedPorch": 0,
        "Neighborhood": "MeadowV",
        "GarageType": "BuiltIn",
        "Foundation": "PConc",
        "Exterior1st": "VinylSd",
        "Exterior2nd": "MetalSd",
        "BsmtFinType1": "GLQ",
        "BsmtFinType2": "Unf",
        "MSZoning": "C (all)",
        "LandContour": "Lvl",
        "MasVnrType": "None",
        "LotShape": "Reg",
        "HouseStyle": "1Story",
        "SaleType": "WD",
        "SaleCondition": "Normal",
        "Electrical": "SBrkr",
        "BldgType": "1Fam",
        "Condition1": "Norm",
        "Heating": "GasA",
        "RoofStyle": "Gable",
        "LotConfig": "Inside"
    }
