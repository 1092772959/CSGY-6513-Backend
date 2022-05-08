# CSGY-6513-Backend

### Prepare Database
We use mongodb as the main database. So please make sure there is a mongodb server running on your machine.(Of course you can upgrade it into a mongo cloud service, which depends on the scale of our data)

Before we actually launch the predicting server, we should pull data through the data center and store it in the mongodb.

```bash
> cd mongo
> ./load_data.sh
```
