from flask import Flask, render_template, request, jsonify
import torch
from IndicTransTokenizer import IndicProcessor
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Initialize model, tokenizer, and processor
ip = IndicProcessor(inference=True)
tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indictrans2-indic-indic-dist-320M", trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/indictrans2-indic-indic-dist-320M", trust_remote_code=True)
tokenizer_eng = AutoTokenizer.from_pretrained("ai4bharat/indictrans2-indic-en-dist-200M", trust_remote_code=True)
model_eng = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/indictrans2-indic-en-dist-200M", trust_remote_code=True)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")
model.to(DEVICE)
model_eng.to(DEVICE)
model.eval()
model_eng.eval()

def real_time_translate(input_text, src_lang="eng_Latn", tgt_lang="hin_Deva"):
    if input_text.strip() == "":
        return ""
    
    if tgt_lang == "eng_Latn":
        # Preprocess the input text
        preprocessed_text = ip.preprocess_batch([input_text], src_lang=src_lang, tgt_lang=tgt_lang, show_progress_bar=False)

        # Tokenize the preprocessed text
        inputs = tokenizer_eng(preprocessed_text, padding="longest", truncation=True, max_length=256, return_tensors="pt").to(DEVICE)

        # Generate translation
        with torch.inference_mode():
            outputs = model_eng.generate(**inputs, num_beams=3, num_return_sequences=1, max_length=256)

        # Decode the generated tokens into text
        with tokenizer_eng.as_target_tokenizer():
            translated_text = tokenizer_eng.batch_decode(outputs.cpu(), skip_special_tokens=True, clean_up_tokenization_spaces=True)

        # Postprocess the translation
        final_translation = ip.postprocess_batch(translated_text, lang=tgt_lang)

    else:
        # Preprocess the input text
        preprocessed_text = ip.preprocess_batch([input_text], src_lang=src_lang, tgt_lang=tgt_lang, show_progress_bar=False)

        # Tokenize the preprocessed text
        inputs = tokenizer(preprocessed_text, padding="longest", truncation=True, max_length=256, return_tensors="pt").to(DEVICE)

        # Generate translation
        with torch.inference_mode():
            outputs = model.generate(**inputs, num_beams=3, num_return_sequences=1, max_length=256)

        # Decode the generated tokens into text
        with tokenizer.as_target_tokenizer():
            translated_text = tokenizer.batch_decode(outputs.cpu(), skip_special_tokens=True, clean_up_tokenization_spaces=True)

        # Postprocess the translation
        final_translation = ip.postprocess_batch(translated_text, lang=tgt_lang)

    return final_translation[0]

@app.route('/')
def home():
    return render_template('page1.html')

@app.route('/page2.html')
def translator():
    return render_template('page2.html')

@app.route('/page3.html')
def record():
    return render_template('page3.html')

@app.route('/page4.html')
def scan():
    return render_template('page4.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    input_text = data.get('text', '')
    src_lang = data.get('source_lang', 'eng_Latn')
    tgt_lang = data.get('target_lang', 'hin_Deva')
    
    translated_text = real_time_translate(input_text, src_lang, tgt_lang)
    
    return jsonify({'translation': translated_text})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
