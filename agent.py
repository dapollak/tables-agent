import asyncio
import os
from agents import Agent, Runner
from agents.mcp.server import MCPServerStdio
from dotenv import load_dotenv
from openai import OpenAI
from schemas import People, SimilarNames
from notion_utils import fetch_notion_titles

load_dotenv()

async def get_number(name: str) -> People:
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@notionhq/notion-mcp-server"],
            "env": {"OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer " + os.getenv("NOTION_KEY") + "\", \"Notion-Version\": \"2022-06-28\" }"}
        },
        client_session_timeout_seconds=10
    ) as server:
        ############## Agents ##############
        # first_agent = Agent(
        #     name="Notion Database uuid and schema fetcher",
        #     instructions="""You use a tool to get the uuid and the schema of a notion database by its title.
        #     """,
        #     mcp_servers=[server],
        #     model="gpt-4.1-nano"
        # )

        query_agent = Agent(
            name="Notion Database query",
            instructions="""
            You query a notion database by title and return the results in a json array.
            Dont use filter_properties url parameter, make it None.
            Use just post-database-query tool, and pass {\"filter\": {\"or\": [{\"property\": \"<property name from prompt>\", \"rich_text\": {\"contains\": \"<value from prompt>\"}}, ... for every value in the given list]}} in the body.
            Print the results as a json array, don't print anything else
            
            extract just the keys under 'properties' from the tool original response and add it without changing their content
            properties.<property_name>.rich_text[0].text.content for 'rich_text' property
            properties.<property_name>.checkbox for 'boolean' property
            properties.<property_name>.title[0].text.content for the title property
            
            if 'results' key in response is empty, return an empty array
            """,
            mcp_servers=[server],
            model="gpt-4.1-nano"
        )

        client = OpenAI()

        ############## Get Database UUID and Schema ##############
        # prompt = f"""
        # Get the uuid of the 'People' database
        # and its schema
        # """
        # result = await Runner.run(first_agent, input=prompt)
        # print(result.final_output)
        # uuid_and_schema = result.final_output
        uuid_and_schema = """
            The UUID of the 'People' database is **1813fc02-0200-80d9-8f9a-c998f398da55**. 

            The schema of the 'People' database includes properties like:
            - Name (title)
            - Table (rich text)
            - Category (select with options such as Core, Friends, Yeala's Family, Daniel's Family)
            - Coming ? (checkbox)
            - Hebrew name (rich text)
            - Invitation Sent (checkbox)
        """

        ############## Get Titles ##############
        titles = fetch_notion_titles("1813fc02-0200-80d9-8f9a-c998f398da55", os.getenv("NOTION_KEY"))
        print(titles)

        ############## Name Similarity ##############
        result = client.responses.create(
            model="gpt-4.1-nano",
            input=[
                {
                    "role": "user",
                    "content": f"""
                    hey, find all similar names in structure to '{name}' from the following list:
                    '{titles}'
                    Return names only from the given list!!!
                    """,
                }
            ],
        )
        result = client.responses.parse(
            model="gpt-4.1-nano",
            input=[
                {
                    "role": "user",
                    "content": result.output_text,
                }
            ],
            text_format=SimilarNames
        )
        print(result.output_parsed)
        if len(result.output_parsed.similar_names) == 0:
            return People(people=[])

        ############## Query Database ##############
        prompt = f"""
        {uuid_and_schema}
        \nQuery the database by 'Name' is one of the following: {result.output_parsed.similar_names}
        Use only one tool call
        """
        result = await Runner.run(query_agent, input=prompt)
        print(result.final_output)

        ############## Parse Response ##############
        response = client.responses.parse(
            model="gpt-4.1-nano",
            input=[
                {
                    "role": "system",
                    "content": """You are a great parser! Help parse the json response according to the provided type.
                    `name` should be a string matched to 'Name' from the json,
                    `hebrew_name` should be a string matched to 'Hebrew name' from the json,
                    `table_number` should be a number matched to 'Table' from the json,
                    `coming` should be a boolean matched to 'Coming ?' from the json""",
                },
                {"role": "user", "content": result.final_output},
            ],
            text_format=People

        )
        print(response.output_parsed)
        if response.output_parsed.people:
            response.output_parsed.people = [person for person in response.output_parsed.people if person.coming]
            return response.output_parsed
        else:
            return People(people=[])

if __name__ == "__main__":
    asyncio.run(get_number("אהרון מנץ"))
