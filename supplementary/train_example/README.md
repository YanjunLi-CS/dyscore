* **Example for generating model based on collect CSV file**

The full flowchart of DyScore training is demonstrated in model_train.py:
1. Read and parse the CSV file
2. Assign training, validation, and test set
3. Use Xgboost to train the model (pre-defined parameters please refer to dyscore.py)
4. Store the trained model to pkl file
5. Use the trained model to predict the test set

* Train the DyScore model with CSV file in example_data

```
python model_train.py --weight_save example.pkl --data_dir example_data
```

* Train the DyScore-MF model with CSV file in example_data_mf

```
python model_train.py --weight_save example_mf.pkl --data_dir example_data_mf --add_feat [20, 21, 22, 23, 24, 25, 26, 27]
```
