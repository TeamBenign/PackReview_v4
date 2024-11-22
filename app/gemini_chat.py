'''
MIT License

Copyright (c) 2024 MD NAZMUL HAQUE, KISHAN KUMAR GANGULY, RAVI 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import numpy as np
import os
import google.generativeai as genai
        
API_KEY = "" #add gemini API key

def get_gemini_feedback(csv_path, user_prompt):
    if csv_path:
        genai.configure(api_key=API_KEY)
        system_instruction= "You are a chatbot designed to assist with job review inquiries at NC State University. Your role is to answer user questions based solely on the job reviews provided to you in a preloaded text file (CSV format). You must adhere to the following rules: Job Review Data Only: Use only the information in the provided text file to generate responses. Do not accept or process job reviews or additional information provided by the user as part of their prompt. Out-of-Scope Queries: If the user asks anything unrelated to the job reviews in the text file, respond with: 'Sorry, I cannot answer this question.' Response Format: Your responses will always consist of two paragraphs: Paragraph 1: A direct and concise answer to the user’s query, based on the reviews in the text file. Paragraph 2: A reference to the specific review(s) and their corresponding _id from the text file that were used to generate the response. Maintain professionalism and clarity in your communication."
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
        sample_txt = genai.upload_file(csv_path)
        try:
            response = model.generate_content(
                [user_prompt, sample_txt],
                generation_config=genai.types.GenerationConfig(
                    # Only one candidate for now.
                    candidate_count=1,
                    max_output_tokens=40000,
                    temperature=0.8,
                ),
            )
            return response.text

        except Exception as e:
            print(f"An error occurred: {e}")
        
        return None
