# Arabic-dialect-classification


Many countries speak Arabic; however, each country has its own dialect, the aim of this project is to build a model that predicts the dialect given the text.

## Data :
- The  dataset has 2 columns, id and dialect (target) , which has 18 classes.
- The “id” column will be used to retrieve the text by calling  this API by a POST request. https://recruitment.aimtechnologies.co/ai-tasks
- The request body must be a JSON as a list of strings, and the size of the list must NOT exceed 1000.
- The API will return a dictionary where the keys are the ids, and the values are the text


Here i Train two models, a machine learning model and a deep learning model.
## Rpo structure:
- Dataset (both)
- Data fetching notebook
- Data pre-processing notebook
- Model Training notebook
- Deployment notebook
