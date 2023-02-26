import whisper

model = whisper.load_model("small")

options = {"fp16": False, "task": "translate"}
result = model.transcribe("testSpedUp.wav", **options)
print(result["text"])