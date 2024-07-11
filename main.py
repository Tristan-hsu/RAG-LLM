from query_data import query_rag
from langchain_community.llms.ollama import Ollama
import argparse    

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""

def main():
    parser = argparse.ArgumentParser(description="程式描述")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # 定義 run 子命令
    parser_query = subparsers.add_parser('query', help='查詢')
    parser_query.set_defaults(func=lambda args: query())
    parser_query = subparsers.add_parser('query_validate', help='查詢與驗證')
    parser_query.set_defaults(func=lambda args: query_validate())   

    args = parser.parse_args()

    # 根據子命令呼叫對應的函式
    if args.command:
        args.func(args)
    else:
        parser.print_help()
    
def query():    
    while True:
        query_text = input("Enter your question or enter exit to stop:\n")
        if query_text == "exit":
            break
        query_rag(query_text)
        print("\n")
            
def query_validate():
    while True:
        question = input("Enter your question or enter exit to stop:\n")
        if question == "exit":
            break
        expected_response = input("Enter your expected response or enter exit to stop:\n")
        query_and_validate(question, expected_response)
            
def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="mistral")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )
        
if __name__ == '__main__':
    main()