from datasets import load_dataset
mfaq_ds =load_dataset("clips/mfaq", "fr")
print(mfaq_ds)
print(mfaq_ds["train"][0:10])