import json

def calculate_quality_metrics(df, clean_df, quarantine_df):
    received_records = len(df)
    valid_records = len(clean_df)
    quarantine_records = len(quarantine_df)

    if received_records > 0:
        valid_percentage = (valid_records / received_records) * 100
        quarantine_percentage = (quarantine_records / received_records) * 100
    else:
        valid_percentage = 0.0
        quarantine_percentage = 0.0

    return {
        "received_records": received_records,
        "valid_records": valid_records,
        "quarantine_records": quarantine_records,
        "valid_percentage": valid_percentage,
        "quarantine_percentage": quarantine_percentage,
    }

def count_quality_issues(quarantine_df):
    issues = quarantine_df["quality_issues"].str.split("|")
    individual_issues = issues.explode()
    issue_counts = individual_issues.value_counts()
    
    return issue_counts.to_dict()

def build_quality_summary(df, clean_df, quarantine_df):
    summary = calculate_quality_metrics(df, clean_df, quarantine_df)
    issue_counts = count_quality_issues(quarantine_df)
    summary.update({"quality_issues": issue_counts})    

    return summary

def save_quality_summary(summary, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, ensure_ascii=False, indent=4)