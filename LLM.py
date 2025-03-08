from typing import Dict, List, Optional, Tuple, Union

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class BaseModel:
    def __init__(self, path: str = '') -> None:
        self.path = path

    def chat(self, prompt: str, history: List[dict]):
        pass

    def load_model(self):
        pass


class InternLM2Chat(BaseModel):
    def __init__(self, path: str = '') -> None:
        super().__init__(path)
        self.load_model()

    def load_model(self):
        print('================ Loading model ================')
        self.tokenizer = AutoTokenizer.from_pretrained(self.path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.path, torch_dtype=torch.float16,
                                                          trust_remote_code=True).cuda().eval()
        print('================ Model loaded ================')

    def chat(self, prompt: str, history: List[dict], meta_instruction: str = '') -> str:
        response, history = self.model.chat(self.tokenizer, prompt, history, temperature=0.1,
                                            meta_instruction=meta_instruction)
        return response, history


class Llama3Chat(BaseModel):
    def __init__(self, path: str = '') -> None:
        super().__init__(path)
        self.load_model()

    def load_model(self):
        print('================ Loading model ================')
        self.tokenizer = AutoTokenizer.from_pretrained(self.path)
        self.model = AutoModelForCausalLM.from_pretrained(self.path, torch_dtype=torch.bfloat16,
                                                          device_map="cuda")
        print('================ Model loaded ================')

    def chat(self, prompt: str, history: List[dict], meta_instruction: str = '') -> str:
        messages = [
            {"role": "system", "content": meta_instruction},
        ]
        for item in history:
            messages.append(item)

        messages.append({"role": "user", "content": prompt})
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device)

        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        outputs = self.model.generate(
            input_ids,
            max_new_tokens=1024,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        response = outputs[0][input_ids.shape[-1]:]
        response = self.tokenizer.decode(response, skip_special_tokens=True)

        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": response})
        return response, history

class QwenChat(BaseModel):
    def __init__(self, path: str = '') -> None:
        super().__init__(path)
        self.load_model()

    def load_model(self):
        print('================ Loading model ================')
        device = "cuda"  # the device to load the model onto
        self.tokenizer = AutoTokenizer.from_pretrained(self.path)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.path,
            torch_dtype=torch.bfloat16,
            device_map=device
        )
        print('================ Model loaded ================')

    def chat(self, prompt: str, history: List[dict], meta_instruction: str = '') -> str:

        prompt = "你是谁"
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(response)
        return response, history

if __name__ == '__main__':
    model_path = '\model\llama_agent'
    model = Llama3Chat(model_path)
    response, _ = model.chat('你好', [])

