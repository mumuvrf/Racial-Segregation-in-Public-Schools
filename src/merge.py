import pandas as pd

def merge_data():
    public_school_data = pd.read_csv('../data/raw/public_school_data.csv', skiprows=6)
    hispanic = pd.read_csv('../data/raw/hispanic_students_data.csv', skiprows=6)

    df = public_school_data.merge(
        hispanic, 
        on=[
            'School ID (12-digit) - NCES Assigned [Public School] Latest available year',
            'School Name',
            'State Name [Public School] Latest available year'
        ], 
        how='left'
    )

    df.to_csv('../data/raw/merged_school_data.csv', index=False)

if __name__ == "__main__":
    merge_data()