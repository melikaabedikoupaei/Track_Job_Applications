# 📄 Track Job Applications with Emails

This script automatically tracks your job application process by extracting important information from your emails and saving it into an organized Excel file (`emails_tracking.xlsx`).

## ✨ Features

- **Track Applications**: Records job applications as they are received.
- **Track Rejections & Interviews**: Updates the status when a rejection or interview invitation is received.
- **Clean Date Formatting**: All dates are converted to **plain strings** (`YYYY-MM-DD HH:MM:SS`) for perfect Excel compatibility.
- **Auto Excel Updates**: Matches new emails with existing entries or adds new rows if needed.

## 🛠 How It Works

- Checks if `emails_tracking.xlsx` exists, or creates it if it doesn't.
- For each incoming email:
  - Extracts company name, job position, sender, subject, body, received time, and rejection reason.
  - Formats received times as simple, timezone-free strings.
  - Updates existing entries or creates new ones depending on the email category.

## 📝 Important Notes

- **Timezone Handling**: No timezone issues — dates are stored as strings.
- **Avoid Duplicates**: Matches records based on company name and job position.
- **Status Tracking**: Supports "Application Received", "Rejected", and "Interview Invitation" statuses.

## 📂 Output

Data is stored in `emails_tracking.xlsx` with the following columns:

- Received Time (Application)
- Received Time (Rejection/Interview)
- Sender
- Subject
- Body
- Company Name
- Job Position
- Status
- Rejection Reason
