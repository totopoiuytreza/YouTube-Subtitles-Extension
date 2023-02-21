const whisper = require('whisper');

model = whisper.load_model("medium");

audio = whisper.load_audio("audio.mp3");
audio = whisper.pad_or_trim(audio);

mel = whisper.log_mel_spectrogram(audio).to(model.device)

probs = model.detect_language(mel)
console.log("Detected language: " + probs.argmax().item())

options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

console.log("Decoded text: " + result.text)