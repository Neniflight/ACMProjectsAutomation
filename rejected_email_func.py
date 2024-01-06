import pandas as pd
import argparse
import re 

def rejected_email_func(accepted_sheet_pathname, total_sheet_pathname):
    def email_verifier(email):
        email = str(email)
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return True
        else:
            return False
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
    accepted_df = pd.read_csv(accepted_sheet_pathname)
    all_df = pd.read_csv(total_sheet_pathname)
    all_emails = get_emails_from_col(all_df)
    accepted_emails = get_emails_from_col(accepted_df)
    not_accepted_emails = [email for email in all_emails if email not in accepted_emails]
    for email in not_accepted_emails:
        print(email)

def main():
    parser = argparse.ArgumentParser(description='Find rejected emails between two spreadsheets.')
    parser.add_argument('file1', help='Path to the first spreadsheet file')
    parser.add_argument('file2', help='Path to the second spreadsheet file')
    
    args = parser.parse_args()
    rejected_email_func(args.file1, args.file2)

if __name__ == "__main__":
    main()