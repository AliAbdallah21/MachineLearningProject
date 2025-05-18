import joblib

preprocessor = joblib.load('models/preprocessor.pkl')

print("Attribute categories:", preprocessor.transformers_[0][1].categories_)
print("Market categories:", preprocessor.transformers_[1][1].categories_)
print("Size categories:", preprocessor.transformers_[2][1].categories_)