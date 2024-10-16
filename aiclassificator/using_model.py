import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

def load_model(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForQuestionAnswering.from_pretrained(model_path)
    return tokenizer, model

def answer_question(context, question, tokenizer, model):
    inputs = tokenizer.encode_plus(question, context, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    
    with torch.no_grad():
        outputs = model(**inputs)
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1

    answer_tokens = inputs['input_ids'][0][answer_start:answer_end]
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(answer_tokens))
    
    return answer

if __name__ == '__main__':
    model_path = './aiclassificator\model'
    tokenizer, model = load_model(model_path)
    
    # Examples
    context1 = "System crashes during high-performance tasks."
    question1 = "What is the main issue reported?"
    answer1 = answer_question(context1, question1, tokenizer, model)

    context2 = "Ethernet cable unplugged message."
    question2 = "What is the main issue reported?"
    answer2 = answer_question(context2, question2, tokenizer, model)

    context3 = "Security credentials not recognized during remote login."
    question3 = "What is the main issue reported?"
    answer3 = answer_question(context3, question3, tokenizer, model)

    context4 = "Ink cartridge empty warning despite recent replacement"
    question4 = "What is the main issue reported?"
    answer4 = answer_question(context4, question4, tokenizer, model)

    print("Respuesta 1:", answer1)
    print("Respuesta 2:", answer2)
    print("Respuesta 3:", answer3)
    print("Respuesta 4:", answer4)