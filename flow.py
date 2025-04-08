from simplegmail import Gmail
from simplegmail.query import construct_query
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel
from typing import Literal, Optional, List
from crews.classification_email_crew.classification_email_crew import ClassificationEmailCrew
from crews.extraction_email_crew.extraction_email_crew import EextractionEmailCrew
import pandas as pd
import os
from datetime import datetime

# Define the EmailState to store the emails as dictionaries
class EmailState(BaseModel):
    emails: List[dict] = []  # List of dictionaries where each dictionary stores info of a single email.

class EmailFlow(Flow[EmailState]):
    
    @start()
    def fetch_unread_emails(self):
        print("===========================================================================")
        print("Starting the structured flow")
        
        # Initialize Gmail client
        client_secret_file = './service_account_key.json'
        gmail = Gmail(client_secret_file)

        # Fetch unread emails from the last day
        query_params = {
            "newer_than": (2, "day"),
            "unread": True
        }
        messages = gmail.get_messages(query=construct_query(query_params))
        
        # Prepare list of emails to store in state
        email_data = []
        for message in messages:
            email_data.append({
                "date": message.date,
                "subject": message.subject,
                "body": message.plain,  # Plain text body
                "sender": message.sender,
            })
        
        # Save email data in the state
        self.state.emails = email_data
        
        # Optionally print out the emails (for debugging purposes)
        print(f"Fetched and saved {len(self.state.emails)} emails.")

    @listen(fetch_unread_emails)
    def categorize_email(self):
        print("===========================================================================")
        print("Categorizing emails...")
        crew = ClassificationEmailCrew().crew()

        # Prepare the list of inputs
        email_contents = [{"email_content": f"Subject: {email['subject']}\n\n{email['body']}"} for email in self.state.emails]

        # Use kickoff_for_each to process all emails
        results = crew.kickoff_for_each(inputs=email_contents)

        # Save the category to each email
        for email, result in zip(self.state.emails, results):
            email["category"] = result.pydantic.category
            print("################################################")
            print(email["category"],email["subject"],email["sender"])

    @listen(categorize_email)
    def remove_irrelevant_emails(self):
        print("===========================================================================")
        print("Removing irrelevant emails...")
        # Keep only emails that are NOT categorized as "Irrelevant"
        self.state.emails = [email for email in self.state.emails if email.get("category") != "Irrelevant"]
        print(f"Remaining emails after removing irrelevant ones: {len(self.state.emails)}")

    @listen(remove_irrelevant_emails)
    def extract_email_info(self):
        print("===========================================================================")
        print("Extracting information from emails...")

        # Assuming the extractor agent is already created in your EmailCrew class
        crew = EextractionEmailCrew().crew()

        # Prepare the list of inputs for extraction
        email_contents = [{"email_content": f"Subject: {email['subject']}\n\n{email['body']}"} for email in self.state.emails]

        # Use kickoff_for_each to extract info from each email
        extraction_results = crew.kickoff_for_each(inputs=email_contents)

        # Save extracted information in the email dictionaries
        for email, extraction_result in zip(self.state.emails, extraction_results):
            extracted_info = extraction_result.pydantic
            email["company_name"] = extracted_info.company_name
            email["job_position"] = extracted_info.job_position
            email["rejection_reason"] = extracted_info.rejection_reason
            print("################################################")
            print(email["category"],email["subject"],email["sender"],email["company_name"],email["job_position"])
    
    @listen(extract_email_info)
    def update_excel_file(self):
        print("===========================================================================")
        print("Updating the Excel file...")

        excel_file_path = "emails_tracking.xlsx"

        # Check if Excel file exists
        if os.path.exists(excel_file_path):
            df = pd.read_excel(excel_file_path)
        else:
            # Create a new DataFrame if file does not exist
            df = pd.DataFrame(columns=[
                "Received Time (Application)",
                "Received Time (Rejection/Interview)",
                "Sender",
                "Subject",
                "Body",
                "Company Name",
                "Job Position",
                "Status",
                "Rejection Reason"
            ])

        # Process each email
        for email in self.state.emails:
            company = email.get("company_name")
            position = email.get("job_position")
            category = email.get("category")
            
            # Convert the received_time to string without timezone
            received_time_raw = email.get("date")
            if received_time_raw:
                received_time = pd.to_datetime(received_time_raw).tz_localize(None)  # remove timezone if exists
                received_time = received_time.strftime("%Y-%m-%d %H:%M:%S")  # convert to string
            else:
                received_time = ""

            sender = email.get("sender")
            subject = email.get("subject")
            body = email.get("body")
            rejection_reason = email.get("rejection_reason")

            # Try to find existing record
            match = df[
                (df["Company Name"] == company) &
                (df["Job Position"] == position)
            ]

            if category == "Application_Received":
                if match.empty:
                    # Create a new application row
                    new_row = {
                        "Received Time (Application)": received_time,
                        "Received Time (Rejection/Interview)": "",
                        "Sender": sender,
                        "Subject": subject,
                        "Body": body,
                        "Company Name": company,
                        "Job Position": position,
                        "Status": "",
                        "Rejection Reason": ""
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            elif category in ["Rejection", "Interview_Invitation"]:
                status = "Rejection" if category == "Rejection" else "Interview_Invitation"
                if not match.empty:
                    # Update existing application row
                    idx = match.index[0]
                    df.at[idx, "Status"] = status
                    df.at[idx, "Received Time (Rejection/Interview)"] = received_time
                    if status == "Rejected":
                        df.at[idx, "Rejection Reason"] = rejection_reason or ""
                else:
                    # No application found, create a new row
                    new_row = {
                        "Received Time (Application)": received_time,
                        "Received Time (Rejection/Interview)": received_time,
                        "Sender": sender,
                        "Subject": subject,
                        "Body": body,
                        "Company Name": company,
                        "Job Position": position,
                        "Status": status,
                        "Rejection Reason": rejection_reason or ""
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Save back to Excel
        df.to_excel(excel_file_path, index=False)
        print(f"Excel file '{excel_file_path}' updated successfully with {len(self.state.emails)} emails.")


# Add the if __name__ == "__main__" block to run the flow
if __name__ == "__main__":
    flow = EmailFlow()
    flow.kickoff()