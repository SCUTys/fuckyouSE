import replicate
import time
import pandas as pd


def dispatch_replicate_api_requests(prompt_list):
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
                    "meta/meta-llama-3-8b-instruct",
                    input=input
                )
                break
            except Exception as e:
                print(f'Error {e}, retry at {time.ctime()}', flush=True)
                time.sleep(20)

        responses.append(''.join(output))
    return responses


def get_summary(df):
    contents = df['内容']
    contents = list(contents)
    contents = ' '.join(contents)
    if len(contents) > 2000:
        contents = contents[:2000]
    contents += '请用简体中文对以上内容进行总结。'
    contents = [contents]
    response = dispatch_replicate_api_requests(contents)
    return response


if __name__ == '__main__':
    columns = ['nickname', 'id', '内容', '时间']
    df = pd.DataFrame(columns=columns)

    # randomly fill in some data
    df.loc[0] = ['nickname', 'id', '内容', '时间']
    df.loc[1] = ['nickname', 'id', '内容', '时间']
    df.loc[2] = ['nickname', 'id', '内容', '时间']
    df.loc[3] = ['nickname', 'id', '内容', '时间']
    df.loc[4] = ['nickname', 'id', '内容', '时间']

    print(*get_summary(df))



