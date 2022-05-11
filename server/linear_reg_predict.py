from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegressionModel
from pyspark.ml.feature import VectorAssembler

import time

spark = SparkSession.builder\
        .master("local")\
        .appName("housing_predict")\
        .config("spark.driver.memory", "16g")\
        .getOrCreate()

ATTR_LABELS = ['crim', 'zn', 'indus', 'chas', 'nox', 'rm', 'age', 'dis', 'rad', 'tax', 'ptratio', 'b', 'lstat']
FEAT_LABELS = ['crim', 'zn', 'indus', 'chas', 'nox', 'rm', 'age', 'dis', 'rad', 'tax', 'ptratio', 'b', 'lstat', 'medv']

class LinearRegServing(object):
    def __init__(self, model_path):
        self.model = LinearRegressionModel.load(model_path)
        self.assembler = VectorAssembler(
            inputCols=ATTR_LABELS,
            outputCol = 'Attributes')

    def to_dataframe(self, data_list):
        return spark.createDataFrame([data_list], FEAT_LABELS)

    def vectorize(self, data):
        df = self.to_dataframe(data)
        return self.assembler.transform(df)
    
    def predict(self, features):
        start_ts = time.time()
        features.append(0)
        
        vec = self.vectorize(features)
        pred = self.model.evaluate(vec)

        ret_dict = dict()
        df = pred.predictions.toPandas()
        for col in df.columns:
            if col == 'Attributes':
                continue
            ret_dict[col] = df[col].values.tolist()[0]
        

        elapse = time.time() - start_ts
        print('Prediction elapse: {:.3f} ms'.format(elapse * 1000))
        return ret_dict


if __name__ == '__main__':
    srv = LinearRegServing("model/linearReg.model")
    ret = srv.predict([0.00632,18,2.31,0,0.538,6.575,65.2,4.09,1,296,15.3,396.9,4.98])
    print(ret)

    ret = srv.predict([0.00632,18,2.31,0,0.538,6.575,65.2,4.09,1,296,15.3,396.9,4.98])
    print(ret)
    