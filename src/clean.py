import pandas as pd
import os

def fill_missing_values(value):
    if value in ["‡", "†", "–", ""]:
        return 0
    return value


def clean_schools_info(schools_info: pd.DataFrame = None) -> pd.DataFrame:
    # Normalize string data
    schools_info["school_name"] = schools_info["school_name"].str.upper()
    schools_info["state_name"] = schools_info["state_name"].str.upper()

    # Remove online schools
    online_schools = schools_info[
        schools_info["school_name"].str.contains("ONLINE") |
        schools_info["school_name"].str.contains("VIRTUAL") |
        schools_info["school_name"].str.contains("CYBER")
    ]

    schools_info = schools_info[~schools_info["school_id"].isin(online_schools["school_id"])]

    return schools_info


def clean_racial_data(
        schools_info: pd.DataFrame = None,
        racial_data: pd.DataFrame = None
    ) -> pd.DataFrame:
    # Filter racial data to only include schools present in schools_info
    racial_data = racial_data[racial_data["school_id"].isin(schools_info["school_id"])]

    # Fill missing values
    racial_data["free_and_reduced_lunch"] = racial_data["free_and_reduced_lunch"].apply(fill_missing_values)
    racial_data["white_students"] = racial_data["white_students"].apply(fill_missing_values)
    racial_data["black_students"] = racial_data["black_students"].apply(fill_missing_values)
    racial_data["hispanic_students"] = racial_data["hispanic_students"].apply(fill_missing_values)
    racial_data["total_students"] = racial_data["total_students"].apply(fill_missing_values)

    # Remove schools with no students
    racial_data["total_students"] = racial_data["total_students"].astype(int)
    racial_data = racial_data[racial_data["total_students"] > 0]

    # Type corrections
    racial_data["white_students"] = racial_data["white_students"].astype(int)
    racial_data["black_students"] = racial_data["black_students"].astype(int)
    racial_data["hispanic_students"] = racial_data["hispanic_students"].astype(int)
    racial_data["free_and_reduced_lunch"] = racial_data["free_and_reduced_lunch"].astype(int)

    # Calculate percentage of students in each racial group
    racial_data["white_pct"] = racial_data["white_students"] / racial_data["total_students"]
    racial_data["white_pct"] = racial_data["white_pct"].fillna(0)

    racial_data["black_pct"] = racial_data["black_students"] / racial_data["total_students"]
    racial_data["black_pct"] = racial_data["black_pct"].fillna(0)

    racial_data["hispanic_pct"] = racial_data["hispanic_students"] / racial_data["total_students"]
    racial_data["hispanic_pct"] = racial_data["hispanic_pct"].fillna(0)

    # Reorder columns for more intuitive structure
    racial_data = racial_data.loc[:, [
        'school_id', 'school_year', 'start_year', 'end_year', 
        'white_students', 'white_pct', 'black_students', 'black_pct',
        'hispanic_students', 'hispanic_pct', 'total_students', 'free_and_reduced_lunch'   
    ]]

    return racial_data


def clean_data():
    schools_info = pd.read_parquet('../data/normalized/schools_info.parquet')
    racial_data = pd.read_parquet('../data/normalized/racial_data.parquet')

    schools_info = clean_schools_info(schools_info)
    racial_data = clean_racial_data(schools_info, racial_data)

    os.makedirs("../data/cleaned", exist_ok=True)
    schools_info.to_parquet('../data/cleaned/schools_info.parquet', index=False)
    racial_data.to_parquet('../data/cleaned/racial_data.parquet', index=False)


if __name__ == "__main__":
    clean_data()