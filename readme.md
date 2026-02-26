Magic: the Gathering LLM RAG Rulings

Ollama RAG implementation of MTG Rules.

LLMs will pull rulings that are parsed from forums, such as Reddit.
They will hallucinate and give wrong rulings and provide dead links to reddit posts that no longer exist.

This implementation will parse the MTG Rules from their official rule book and insert it into a [vector database](http://trychroma.com).
Using RAG we can run a [low resource LLM](https://ollama.com/library/gemma3) locally and get better results than the base model.

to run:

```
pip3 install -r requirements.txt

python3 ./main.py
```
