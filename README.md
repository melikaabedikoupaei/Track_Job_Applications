# 📄 Job Application Tracker (Automated)

I was applying to so many companies that it became really hard to keep track of everything manually.  
That's why I decided to **automate** the process.

This script reads my job-related emails, extracts important information (like company, position, status), and saves everything into an organized Excel file.

### 🛠 What it does

- Tracks when I apply to a company (Application Received).
- Tracks when I get a rejection or interview invitation.
- Saves everything neatly into an Excel sheet: `emails_tracking.xlsx`.
- Makes sure all dates are clean (no messy timezone problems).

### 🔥 Why I built it

- I wanted an **easy way to track all applications** without spending hours updating spreadsheets manually.
- The next step is to **build a simple UI** to visualize KPIs (Key Performance Indicators), like:
  - How many applications I sent
  - How many interviews I got
  - Rejection rate
  - Which companies responded fastest

### 📂 Excel Output

The file stores the following info:

- Received Time (Application)
- Received Time (Rejection/Interview)
- Sender
- Subject
- Body
- Company Name
- Job Position
- Status
- Rejection Reason
