# from openai import OpenAI
# from app.core.settings import settings
# import json
# from typing import List, Dict, Any
# from app.schemas.response import CleanContactDetailsResponse
# from pydantic import BaseModel
# from loguru import logger
# from app.schemas.warmup_campaign import WarmupEmailSchema


# class AIService:
#     def __init__(self):
#         self.client = OpenAI(api_key=settings.openai_api_key)

#     # -----------------------------GET AI RESPONSE ----------------------------- #
#     def get_ai_response(self, prompt: str, schema):
#         try:
#             response = self.client.chat.completions.create(
#                 model="gpt-4.1-nano",
#                 messages=[
#                     {"role": "user", "content": prompt}
#                 ],
#                 response_format={"type": "json_object"},
#                 max_tokens=4000,
#                 temperature=0.1
#             )

#             content = response.choices[0].message.content
#             if content is None:
#                 logger.error("Received null content from AI response")
#                 return None
#             parsed = schema.parse_raw(content)
#             logger.success(f"AI Response parsed successfully {parsed}")
#             return parsed

#         except Exception as e:
#             logger.error(f"Error: {str(e)}")
#             return None

#     async def load_knowledge_base(self, file_path: str):
#         """
#         A helper method to load the knowledge base into the RAG service.
#         This can be called from an API endpoint upon file upload.
#         """

#     # -----------------------------GET CLEAN CONTACT DETAILS ----------------------------- #
#     async def get_clean_contact_details(self, contact_details: List[Dict[str, Any]]):
#         prompt = f"""
#             You are a data-cleaning assistant. You will be given a list of contact details, each containing fields like name, email, role, and company.

#             Your task is to clean the data by:
#             1. Ensuring the name field contains only the person's actual name (e.g., if the name is "John Microsoft", correct it to "John")
#             2. Removing any company names, job titles, or irrelevant words from the name field
#             3. Ensuring the role and company fields are accurate and not mixed into the name
#             4. Keep all original IDs intact
#             5. Return ALL contacts in the cleaned format

#             Contact details to clean:
#             {json.dumps(contact_details, indent=2)}

#             IMPORTANT: Return ALL contacts in this exact JSON format:
#             {{
#             "cleaned_contacts": [
#                 {{
#                 "id": 1,
#                 "name": "Cleaned Name",
#                 "email": "email@example.com",
#                 "role": "Role",
#                 "company": "Company"
#                 }},
#                 {{
#                 "id": 2,
#                 "name": "Another Name",
#                 "email": "another@example.com",
#                 "role": "Another Role",
#                 "company": "Another Company"
#                 }}
#             ]
#             }}

#             Make sure to include ALL contacts from the input list.
# """

#         response = self.get_ai_response(prompt, CleanContactDetailsResponse)
#         return response

#     # -----------------------------GET WARMUP EMAIL ----------------------------- #
#     async def get_warmup_email(self, name: str, email: str, role: str, company: str):
            
#         content_prompt = f"""
#             Act as a market research expert who is 20+ years experienced in solving tough market research problems in the industry of the company we are mentioning.

#             Craft a concise and compelling cold email without citations to "name": {name},
#                         "email": {email},
#                         "role": {role},
#                         "company": {company}, pitching Consainsights (https://www.consainsights.com/) Market Research services (https://www.consainsights.com/custom-research) respectively to the contact, role, and company mentioned.  

#             Ask necessary list of throught-provoking market research pain point addressing questions relevant to the role (measurable objectives - read this book "the science of sales success"), industry(pressing unsolved market research problems), (combined)  along with focusing on most-convincing social proof which is like a promise (not mentioning any company, but just numbers and impact we created for a similar company - no big claims as we are a very small company(keep it realistic))

#             Give the most convenient CTA for contact to get in touch with us back - should be most convenient yet create compulsion to respond back positively

#             The subject line should be brief and attention-grabbing, prominently starting and featuring "Company name." 

#             This is for your reference to draft an exceptional offer, but never mention in the email: For creating an exciting offer personalized to this contact and company: refer to $100Mn leads and $100Mn offers by Alex Hormozi

#             Writing guidelines:

#             The prime focus and objective of this email is to get a reply at any cost.

#             Rules:
#             1. No unnecessary lines
#             2. High readability score
#             3. Strict No "—" in email subject line and body
#             4. Thought leadership content (thought-provoking industry-specific)
#             5. simple yet understandable language (class 3 standard) 
#             6. Very humanized content
#             7. Do not introduce - straight away get to the point
#         """
#         total_tokens_used = 0
#         try:
#             # Step 1: Get content from GPT-4o-mini with web search
#             response = self.client.responses.create(
#                 model="gpt-4o",
#                 tools=[{"type": "web_search_preview"}],
#                 input=content_prompt,
#                 temperature=0.1
#             )
#             raw_content = response.output_text
#             if hasattr(response, 'usage') and response.usage:
#                 web_search_tokens = response.usage.total_tokens
#                 total_tokens_used += web_search_tokens
#                 logger.info(
#                     f"Web search tokens used for {email}: {web_search_tokens}")

#             # Step 2: Use GPT-4kno.1-nano to structure content and add basic styling
#             styling_prompt = f"""Convert this email content to JSON with basic HTML styling:

#             {raw_content}

#             CRITICAL REQUIREMENTS:
#             - NO signature or sender details in the body (will be added externally)
#             - Remove any "Best regards", "Sincerely", or closing phrases
#             - Remove any signature lines or sender information
#             - End the email content with the main message only

#             Apply these styling rules:
#             - Use 14px Georgia font
#             - Black text (#000000) 
#             - Basic paragraph tags and line breaks
#             - Simple <strong> tags for emphasis
#             - Black underlined links
#             - NO outer container styling

#             Return ONLY this JSON format:
#             {{
#             "subject": "Email subject here",
#             "body": "<p>Hi {name},</p><p>Email content with basic HTML tags...</p>"
#             }}"""

#             structured_output = self.client.chat.completions.create(
#                 model="gpt-4.1-nano",
#                 messages=[{"role": "user", "content": styling_prompt}],
#                 response_format={"type": "json_object"},
#             )
#             if hasattr(structured_output, 'usage') and structured_output.usage:
#                 structure_tokens = structured_output.usage.total_tokens
#                 total_tokens_used += structure_tokens
#                 logger.info(
#                     f"Structure output tokens used for {email}: {structure_tokens}")

#             json_content = structured_output.choices[0].message.content
#             logger.info(f"Generated JSON for {email}: {json_content}")

#             try:
#                 if json_content is None:
#                     logger.error("Received null JSON content")
#                     return None
#                 parsed = WarmupEmailSchema.parse_raw(json_content)

#                 # Step 3: Add outer styling and sender details externally
#                 styled_body = self._add_external_styling_and_signature(
#                     parsed.body, name)
#                 parsed.body = styled_body

#                 logger.success(
#                     f"AI Response with optimized token usage for {email}")
#                 logger.info(
#                     f"Total tokens used for {email}: {total_tokens_used} (Web Search: {web_search_tokens if 'web_search_tokens' in locals() else 'N/A'}, Structure: {structure_tokens if 'structure_tokens' in locals() else 'N/A'})")
#                 return parsed
#             except Exception as json_error:
#                 logger.error(f"JSON parsing failed for {email}: {json_error}")
#                 logger.error(f"Raw JSON content: {json_content}")
#                 return None
#         except Exception as e:
#             logger.error(
#                 f"Error in get_warmup_email with optimized token usage: {e}")
#             logger.error(
#                 f"Tokens used before error for {email}: {total_tokens_used}")
#             return None

#     def _add_external_styling_and_signature(self, body_content: str, recipient_name: str) -> str:
#         """Add external styling wrapper and sender signature"""

#         # Define the outer styling
#         outer_styles = """
#         <style>
#             body {
#                 font-family: Georgia, 'Times New Roman', serif;
#                 font-size: 13px;
#                 line-height: 1.5;
#                 color: #000000;
#                 margin: 0;
#                 padding: 0;
#                 background-color: #f5f5f5;
#             }
#             .email-container {
#                 max-width: 600px;
#                 margin: 40px auto;
#                 background-color: #ffffff;
#                 padding: 40px;
#                 border: 1px solid #e0e0e0;
#             }
#             p {
#                 font-size: 13px;
#                 margin: 15px 0;
#                 color: #000000;
#             }
#             strong {
#                 font-size: 13px;
#                 color: #000000;
#             }
#             a {
#                 color: #000000;
#                 text-decoration: underline;
#             }
#             .signature {
#                 font-size: 13px;
#                 color: #444444;
#                 font-weight: bold;
#                 margin-top: 30px;
#                 border-top: 1px solid #e0e0e0;
#                 padding-top: 20px;
#             }
#         </style>
#         """

#         # Define the sender signature
#         signature = """
#         <div class="signature">
#             Cillian Brett<br>
#             Sales Manager<br>
#             Consainsights
#         </div>
#         """

#         # Combine everything into full HTML email
#         full_email = f"""<!DOCTYPE html>
# <html>
# <head>
#     {outer_styles}
# </head>
# <body>
#     <div class="email-container">
#         {body_content}
#         {signature}
#     </div>
# </body>
# </html>"""

#         return full_email
