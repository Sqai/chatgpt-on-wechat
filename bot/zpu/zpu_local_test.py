from zhipuai import ZhipuAI
from operator import methodcaller

import json

tools = [
    {
        "type": "function",
        "function": {
            "name": "query_book_info",
            "description": "根据用户提供的信息，查询对应的书籍",
            "parameters": {
                "type": "object",
                "properties": {
                    "bookTitleMark": {
                        "type": "string",
                        "description": "书名或文件名",
                    },
                    "author": {
                        "type": "string",
                        "description": "作家名称",
                    },
                    "publishingHouse": {
                        "type": "string",
                        "description": "出版社名称",
                    },
                    "date": {
                        "type": "string",
                        "description": "要查询的书籍的出版日期",
                    },
                },
                "required": ["bookTitleMark"],
            },
        }
    }
]

messages = [
    {
        "role": "user",
        "content": "我要查询红楼梦这本书。"
    }
]

books = [
    {
        "name": "红楼梦",
        "author": "曹雪芹, 高鹗, 程伟元",
        "publishingHouse": "人民文学出版社",
        "date": "2001"
    }

]


def query_book_info(bookTitleMark, author, publishingHouse, date):
    try:
        bookTitleMark = str(bookTitleMark)
    except:
        return "不知道"
    # 在query_book_info中循环遍历books集合，使用bookTitleMark,author,publish、bingHou..作为条件，要注意除了bookTitleMark外其他参数都可能为空。
    for book in books:
        name = book.get("name")
        author = book.get("author")
        publishingHouse = book.get("publishingHouse")
        date = book.get("date")
        if name == bookTitleMark:
            return book
    return None


def run():
    client = ZhipuAI(api_key="5354ded014ca91b7afbc81800fc9b7dd.rQtyme8QENaAiQN0")  # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages,
        tools=tools
    )
    print(response)
    calls = response.choices[0].message.tool_calls
    if len(calls) > 0:
        for call in calls:
            if call.function.name == "query_book_info":
                jsonData = json.loads(call.function.arguments)
                resultJson = {'bookTitleMark': '', 'author': '', 'publishingHouse': '', 'date': ''}
                resultJson.update(jsonData)
                values_tuple = tuple(resultJson.values())
                book = globals()['query_book_info'](*values_tuple)
                print(book)
    print("none")


if __name__ == "__main__":
    # model='glm-4' created=1706957216 choices=[CompletionChoice(index=0, finish_reason='tool_calls', message=CompletionMessage(content=None, role='assistant', tool_calls=[CompletionMessageToolCall(id='call_8356033834230353403', function=Function(arguments='{"bookTitleMark":"红楼梦"}', name='query_book_info'), type='function')]))] request_id='8356033834230353403' id='8356033834230353403' usage=CompletionUsage(prompt_tokens=192, completion_tokens=17, total_tokens=209)
    run()
    # jsonStr = '{"bookTitleMark":"红楼梦"}'
    # jsonData = json.loads(jsonStr)
    # resultJson = {'bookTitleMark':'','author':'','publishingHouse':'','date':''}
    # resultJson.update(jsonData)
    # print(resultJson)
    # values_tuple = ('红楼梦','','','')
    # locals()['query_book_info'](*values_tuple)
    print('')
