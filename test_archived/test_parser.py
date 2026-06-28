from llm.parser import ResponseParser
response = """Sure!
```json
{"dataset_type" : "Retail",
 "metrics" : ["Sales", "Profit"]
}
 """

parsed = ResponseParser.parse_json(response)

print(parsed)