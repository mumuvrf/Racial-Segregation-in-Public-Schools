import pandas as pd
import os

def extract_schools_info(df: pd.DataFrame):
    schools_info = df.loc[:, 
        ["School ID (12-digit) - NCES Assigned [Public School] Latest available year",
        "School Name", "State Name [Public School] Latest available year"]
    ]

    schools_columns = {
        "School ID (12-digit) - NCES Assigned [Public School] Latest available year" : "school_id",
        "School Name": "school_name",
        "State Name [Public School] Latest available year": "state_name"
    }

    schools_info = schools_info.rename(columns=schools_columns)
    schools_info['school_id'] = schools_info['school_id'].astype(str)

    return schools_info


def extract_racial_data(df: pd.DataFrame):
    school_years = [
        '2008-09', '2009-10', '2010-11', '2011-12',
        '2012-13', '2013-14', '2014-15', '2015-16',
        '2016-17', '2017-18', '2018-19', '2019-20',
        '2020-21', '2021-22', '2022-23', '2023-24',
        '2024-25'
    ]

    slices = []
    for school_year in school_years:
        columns = {
            "School ID (12-digit) - NCES Assigned [Public School] Latest available year": "school_id",
            f"White Students [Public School] {school_year}": "white_students",
            f"Black or African American Students [Public School] {school_year}": "black_students",
            f"Hispanic Students [Public School] {school_year}": "hispanic_students",
            f"Total Race/Ethnicity [Public School] {school_year}": "total_students",
            f"Free and Reduced Lunch Students [Public School] {school_year}": "free_and_reduced_lunch"
        }
        df_slice = df.loc[:, columns.keys()]
        df_slice = df_slice.rename(columns=columns)
        df_slice["school_year"] = school_year
        slices.append(df_slice)

    racial_data = pd.concat(slices, ignore_index=True)
    racial_data['school_id'] = racial_data['school_id'].astype(str)

    return racial_data


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    schools_info = extract_schools_info(df)
    racial_data = extract_racial_data(df)

    os.makedirs("../data/normalized", exist_ok=True)
    schools_info.to_parquet('../data/normalized/schools_info.parquet', index=False)
    racial_data.to_parquet('../data/normalized/racial_data.parquet', index=False)


if __name__ == "__main__":
    df = pd.read_csv('../data/raw/merged_school_data.csv')
    normalize_data(df)