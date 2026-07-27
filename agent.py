import os
import sqlite3
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Automatically load secrets from your hidden .env file
load_dotenv()

# 2. Instantiate the blazing-fast Llama model via Groq 
# It automatically looks for os.environ["GROQ_API_KEY"] behind the scenes
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

def run_local_sql(query: str):
    """Executes a SQL query against the local database safely."""
    try:
        conn = sqlite3.connect("company.db")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        return f"Database execution error: {str(e)}"

def query_database(user_question: str):
    try:
        system_prompt = (
            "You are a strict Text-to-SQL translator. Given a user question, return ONLY a valid, executable SQLite query "
            "and nothing else. Do not wrap the code in markdown block format. Do not write explanations.\n\n"
            "Database Schema:\n"
            "Table: employees\n"
            "Columns: id (INTEGER), name (TEXT), department (TEXT), salary (INTEGER)\n"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}")
        ])
        
        chain = prompt | llm
        
        # Step A: Generate the raw SQL statement from Groq
        ai_message = chain.invoke({"question": user_question})
        generated_sql = ai_message.content.strip().replace("```sql", "").replace("```", "")
        
        print(f"\n[Generated SQL]: {generated_sql}")
        
        # Step B: Run the SQL query locally against our company.db file
        db_data = run_local_sql(generated_sql)
        print(f"[Database Raw Results]: {db_data}")
        
        # Step C: Parse and present all data rows safely
        if db_data and isinstance(db_data, list):
            try:
                formatted_results = []
                for row in db_data:
                    row_string = ", ".join(str(item) for item in row)
                    formatted_results.append(row_string)
                
                final_output = " | ".join(formatted_results)
                return f"The database answer is: **{final_output}**"
                
            except Exception:
                return "Query ran successfully but returned empty columns."
        return f"Query returned no data matching that filter: {db_data}"
        
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    q = "Who has the highest salary in the Engineering department?"
    print(f"\nQuestion: {q}")
    print(f"Answer: {query_database(q)}")
