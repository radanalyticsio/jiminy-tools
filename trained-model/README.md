# Trained model (MongoDB)

This directory contains a pre-trained Apache Spark ALS model serialized
as MongoDB documents.

The model was trained using the [small MovieLens](http://files.grouplens.org/datasets/movielens/ml-latest-small-README.html)
dataset with the parameters:

 * `rank = 8`
 * `lambda = 0.01`
 * `iterations = 2`
 * `model_version = 1`
 
This model is only intended for testing purposes (namely of [jiminy-predictor](https://github.com/radanalyticsio/jiminy-predictor)).

## Setup

`mongorestore` can be used to install the model. For instance,

```
mongorestore -d ./models models
```

will restore the `models` directory into the MongoDB `models` database.

After configuring MongoDB as the model store, according to
the steps provided in [jiminy-predictor](https://github.com/radanalyticsio/jiminy-predictor), 
this model is ready to be used for rating and ranking predictions. 


