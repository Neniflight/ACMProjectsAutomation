import pandas as pd
import argparse
import re 

"""
Function to return emails that were rejected by ACM Projects. It will automatically
detect email address columns given the sheets and only extract rejected emails

Inputs:
- files: strings that are filepaths. Make sure to provide at least 2 spreadsheets
Additionally, the first file should be the sheet containing all applicants and the next
sheets should contain the team sheets. 

Output:
- prints emails along with the number of rejections
"""#input files in order of total sheet first and then the accepted sheets
def rejected_email_func(files):
    # accepted_sheet_pathname, total_sheet_pathname
    if len(files) < 2:
        print("Please provide at least two spreadsheet files as csv")
    def email_verifier(email):
        email = str(email)
        # email pattern string
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return True
        else:
            return False
    # function to find the email columns
    def find_columns_with_emails(df):
        if df.shape[0] == 0:
            raise ValueError("No rows in df")
        columns_name = list(df.columns)
        columns_with_emails = []
        found_email = False
        row_number = 0
        while found_email == False:
            for i in range(df.shape[1]):
                cell_value = df.iloc[row_number, i]
                if email_verifier(cell_value):
                    columns_with_emails.append(columns_name[i])
                    found_email = True
            row_number += 1
        return columns_with_emails
    def get_emails_from_col(df):
        emails = []
        list_col = find_columns_with_emails(df)
        for col in list_col:
            emails += list(df[col])
        emails = list(set(emails))
        return emails
    
    all_df = pd.read_csv(files[0])
    accepted_dfs = []
    for i in range(1, len(files)):
        accepted_dfs.append(pd.read_csv(files[i]))

    all_emails = get_emails_from_col(all_df)
    accepted_emails = [get_emails_from_col(accepted_df) for accepted_df in accepted_dfs]
    accepted_emails = [item for sublist in accepted_emails for item in sublist]
    not_accepted_emails = [email for email in all_emails if email not in accepted_emails]
    print("Number of rejected emails: " + len(not_accepted_emails))
    for email in not_accepted_emails:
        print(email)

def main():
    parser = argparse.ArgumentParser(description='Find rejected emails between two spreadsheets.')
    parser.add_argument('files', nargs="+", help='Path to the first spreadsheet file')
    
    args = parser.parse_args()
    rejected_email_func(args.files)

if __name__ == "__main__":
    main()