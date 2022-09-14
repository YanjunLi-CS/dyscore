* **Example for using DyScore/DyScore-MF model with provided CSV file**

The full flowchart of DyScore training is demonstrated in model_train.py:
1. Read and parse the CSV file
2. Load pre-trained models (weight file)
3. Use three pre-trained models to perform the prediction


* Install dependent modules (Python3)
```
pip install -r requirments.txt
```


* Predict with DyScore model based on input.csv (python3)

```
./model_predict input.csv <DOWNLOAD_DIR>
```

* Predict with DyScore-MF model based on input.csv (python3)

```
./model_predict input_mf.csv <DOWNLOAD_DIR>
```
