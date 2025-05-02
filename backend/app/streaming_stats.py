from pathlib import Path
from typing import Optional, Dict
import pandas as pd
import calendar
import pycountry


def load_data(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep="\t")
    df["Sale Month"] = pd.to_datetime(df["Sale Month"], errors="coerce")
    df = df.dropna(subset=["Sale Month"])
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    return df


def get_country_name(code):
    country = pycountry.countries.get(alpha_2=code)
    return f"{country.name} ({code})" if country else code

def calculate_stats(
    file_path: Path,
    store: Optional[str] = None,
    year: Optional[str] = None,
    month: Optional[str] = None,
    country: Optional[str] = None,
) -> Dict:
    df = load_data(file_path)

    available_stores = sorted(df["Store"].dropna().unique().tolist())

    available_years = sorted(
        df["Sale Month"].dt.year.dropna().unique().tolist(), reverse=True
    )

    available_months = [
        {"key": month, "name": calendar.month_name[month]}
        for month in sorted(df["Sale Month"].dt.month.dropna().unique().tolist())
    ]

    available_countries = [
        {"key": code, "name": get_country_name(code)}
        for code in sorted(df["Country of Sale"].dropna().unique().tolist())
    ]

    filtered_df = df.copy()

    if store and store.lower() != "any":
        filtered_df = filtered_df.loc[filtered_df["Store"] == store]

    if year and year.lower() != "any":
        filtered_df = filtered_df.loc[filtered_df["Sale Month"].dt.year == int(year)]

    if month and month.lower() != "any":
        filtered_df = filtered_df.loc[filtered_df["Sale Month"].dt.month == int(month)]

    if country and country.lower() != "any":
        filtered_df = filtered_df.loc[filtered_df["Country of Sale"] == country]
    filtered_streams = int(filtered_df["Quantity"].sum())

    return {
        "filters": {
            "available_stores": available_stores,
            "available_years": available_years,
            "available_months": available_months,
            "available_countries": available_countries,
        },
        "store": store,
        "year": year,
        "month": month,
        "country": country,
        "streams": filtered_streams,
    }
