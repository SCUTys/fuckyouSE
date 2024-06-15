import replicate
import time
import pandas as pd
import sqlite3


def dispatch_replicate_api_requests(prompt_list):
    """
        prompt_list: python list of prompts  ** must be a list!!!***
        return: python list of responses
    """
    if not isinstance(prompt_list, list):
        raise Exception("The prompt is not in a list, this can cause unexpected output.")
    responses = []
    for message in prompt_list:
        while True:
            try:
                input = {
                    "top_p": 0.95,
                    "prompt": f"{message}",
                    "temperature": 0.7,
                    "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                    "presence_penalty": 0,
                    "max_new_tokens": 1024,
                }
                output = replicate.run(
                    "meta/meta-llama-3-70b-instruct",
                    input=input
                )
                break
            except Exception as e:
                print(f'Error {e}')
                output = []
                break
                # print(f'Error {e}, retry at {time.ctime()}', flush=True)
                # time.sleep(20)

        responses.append(''.join(output))
    return responses


def get_summary(database_loc, product_id=None):
    """
        database_loc: dir of the database
        return: python list of responses
    """
    if product_id is None:
        raise Exception("Product id is not provided.")
    # get product table from database
    conn = sqlite3.connect(database_loc)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product WHERE product_id = ?", (product_id,))

    row = cursor.fetchone()
    comments = row[3]

    if len(comments) > 2000:
        comments = comments[:2000]

    contents = '以下是某购物网站上的用户评论：\n'
    contents += comments + '\n'
    contents += '请获取评论中出现的优缺点，并使用优点：{}；缺点：{}的格式进行总结。必须使用简体中文进行回复。不要在回复中出现任何英文单词。'
    contents = [contents]
    responses = dispatch_replicate_api_requests(contents)
    print("LLM response: ",responses)
    return responses


if __name__ == '__main__':
    database_loc = r'..\SE_project\jd_comments.sqlite3'
    response = get_summary(database_loc)
    print(response)



