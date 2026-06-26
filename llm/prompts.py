import json

SYSTEM_PROMPT = '''you are an expert Senior data Scientist.
Your job is to understand datasets, reason about business problems, suggest meaningful analyses and generate insights
Always respond ONLY in valid JSON whenever requested.

Never include markdowns
Never include explanations outside JSON
'''

def buld_planner_prompt(dataset_profile, column_profiles):
    profile_json  = json.dumps(dataset_profile , indent = 2, default = str)
    columns_json = json.dumps(column_profiles, indent = 2, default= str)
    prompt = f""" You are given a metafdata about the tabular dataset.
Your task is to understand the dataset and prepare an analysis plan.
Dataset profile {profile_json}
Column profiles {column_profiles}
Return ONLY valid JSON in the following format.print
{{
"dataset_type" : "",
"business_domain" : "",
"possible_target" : "",
"metrics" : [],
"dimensions" : [],
"identifiers" : [],
"recommended_analyses" : [RecursionError{{
"analysis" : "",
"priority" : 1,
"reason" : ""
}}
],
"summary" : ""
}}

Rules
1. Infer dataset type.
2. Identify business metrics.
3. Identify dimensions. 
4. Identify identifiers. 
5. Guess possible target column. 
6. Recommend analyses.
7. Do not invent columns. 
8. Output JSON only.
"""
    return prompt

def build_summary_prompt(insights):
    insights_json = json.dumps(insights, indent = 2, deault = str)
    prompt = f'''Write a concise executive summary. Maximum 250 words. Inputs
    {insights_json}
    Return JSON
    {{ "Summary" : ""}}
    '''

    return prompt

def build_chat_prompt(question, context):
    context_json = json.dumps(context, indent = 2, default = str)
    prompt = f'''Dataset Context {context_json}
                Question {question}
                Answer only using the supplied context.
                If the answer cannot be inferred, say so explicitly.
                Return plain text
                '''
    return prompt

