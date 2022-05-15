# CSGY-6513-Backend

### Prepare Database
We use mongodb as the main database. So please make sure there is a mongodb server running on your machine.(Of course you can upgrade it into a mongo cloud service, which depends on the scale of our data)

Before we actually launch the predicting server, we should pull data through the data center and store it in the mongodb.

```bash
> cd mongo
> ./load_data.sh
```



### Prepare Environment

Python: 3.7

Java: 8

Spark: 2.4.7

Kafka: 2.13-3.1.0

Mongodb: 5.0.3

#### Python

```bash
> pip install -r requirements.txt
```

#### Java

```bash
> export JAVA_HOME=#{your java directory}
```

#### Spark

```bash
> export SPARK_HOME=#{your spark directory}
```

#### Kafka

```bash
> cd #{your kafka directory}
> bin/zookeeper-server-start.sh config/zookeeper.properties #luanch zookeeper for kafka broker coordination
```

start a new terminal

```bash
> bin/kafka-server-start.sh config/server.properties
```



### Architecture

#### Single Prediction

![Prediction.drawio (1)](README.assets/Prediction.drawio (1).png)

#### Batch Prediction

![Barch Prediction.drawio](README.assets/Barch Prediction.drawio.png)

### API Design

#### HTTP

- Single prediction

Request:

<img src="README.assets/image-20220512122216565.png" alt="image-20220512122216565" style="zoom:80%;" />

Response:

```json
{
    "code": 0,
    "data": {
        "age": 65.2,
        "b": 396.9,
        "chas": 0.0,
        "crim": 0.00632,
        "dis": 4.09,
        "indus": 2.31,
        "lstat": 4.98,
        "medv": 0,
        "nox": 0.538,
        "prediction": 30.025022480537096, // the result our user need 
        "ptratio": 15.3,
        "rad": 1.0,
        "rm": 6.575,
        "tax": 296.0,
        "zn": 18.0
    },
    "message": "succeed"
}
```



- Batch prediction

Request:

![image-20220512122320329](README.assets/image-20220512122320329.png)

CSV format:

according to attributes ['crim', 'zn', 'indus', 'chas', 'nox', 'rm', 'age', 'dis', 'rad', 'tax', 'ptratio', 'b', 'lstat']

```
0.00632,18,2.31,0,0.538,6.575,65.2,4.09,1,296,15.3,396.9,4.98
0.02731,0,7.07,0,0.469,6.421,78.9,4.9671,2,242,17.8,396.9,9.14
```



Get task results with task id:

![image-20220512123920114](/Users/xiuwenli/Document/nyu/2022Spring/bigdata/CSGY-6513-Backend/README.assets/image-20220512123920114.png)

Response:

```json
{
    "code": 0,
  	"message": "succeed",
    "data": [
        {
            "age": 65.2,
            "b": 396.9,
            "chas": 0,
            "crim": 0.00632,
            "dis": 4.09,
            "indus": 2.31,
            "lstat": 4.98,
            "nox": 0.538,
            "prediction": 30.025022480537096,
            "ptratio": 15.3,
            "rad": 1,
            "rm": 6.575,
            "tax": 296,
            "zn": 18
        },
        {
            "age": 78.9,
            "b": 396.9,
            "chas": 0,
            "crim": 0.02731,
            "dis": 4.9671,
            "indus": 7.07,
            "lstat": 9.14,
            "nox": 0.469,
            "prediction": 25.471234598995597,
            "ptratio": 17.8,
            "rad": 2,
            "rm": 6.421,
            "tax": 242,
            "zn": 0
        }
    ]
}
```



#### Kafka Message

```json
{
  "task_id": "934123916882940396",
}
```



#### MongoDB Collection

- Task pending/predicting

```
{
  "task_id": "934123916882940396",
  "status": 1,
  "input_list": [ 
    [ 0.00632, 18, 2.31, 0, 0.538, 6.575, 65.2, 4.09, 1, 296, 15.3, 396.9, 4.98 ], 
    [ 0.02731, 0, 7.07, 0, 0.469, 6.421, 78.9, 4.9671, 2, 242, 17.8, 396.9, 9.14 ],
  ],
}
```



- Task succeeded

```json
{
  "task_id": "934123916882940396",
  "status": 0,
  "input_list": [ 
    [ 0.00632, 18, 2.31, 0, 0.538, 6.575, 65.2, 4.09, 1, 296, 15.3, 396.9, 4.98 ], 
    [ 0.02731, 0, 7.07, 0, 0.469, 6.421, 78.9, 4.9671, 2, 242, 17.8, 396.9, 9.14 ],
  ],
  "prediction": [
    30.025022480537096,
    25.471234598995597,
  ]
}
```

