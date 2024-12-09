import pandas as pd
import json
import numpy as np
from typing import Optional, Dict


class PostalDataProcessor:
    """Class for processing and enriching property data using postal and demographic data."""
    
    def __init__(self, property_data_path: str, postal_data_path: str, ins_to_postal_path: str):
        """
        Initialize the processor with file paths.
        
        Args:
            property_data_path (str): Path to the CSV file containing property data.
            postal_data_path (str): Path to the Excel file containing postal data.
            ins_to_postal_path (str): Path to the JSON file mapping Code_INS to postal codes.
        """
        self.property_data = pd.read_csv(property_data_path)
        self.postal_data = pd.read_excel(postal_data_path)
        self.ins_to_postal = self._load_json(ins_to_postal_path)
        self.postal_data_dict = self._create_postal_data_dict()

    @staticmethod
    def _load_json(json_path: str) -> Dict:
        """Load a JSON file and return its content."""
        with open(json_path, 'r') as f:
            return json.load(f)
    
    def _create_postal_data_dict(self) -> Dict:
        """Convert postal data to a dictionary with 'Code_INS' as the key."""
        return self.postal_data.set_index('Code_INS')[['Population', 'Wealth_Index', 'Density']].to_dict(orient='index')
    
    def _get_ins_code(self, postal_code: int) -> Optional[int]:
        """Retrieve the Code_INS for a given postal code."""
        for ins_code, postal_list in self.ins_to_postal.items():
            if str(int(postal_code)) in postal_list:
                return int(ins_code)
        return None
    
    def _get_population(self, ins_code: int) -> Optional[int]:
        """Retrieve the population for a given INS code."""
        return self.postal_data_dict.get(ins_code, {}).get('Population')
    
    def _get_wealth_index(self, ins_code: int) -> Optional[float]:
        """Retrieve the wealth index for a given INS code."""
        return self.postal_data_dict.get(ins_code, {}).get('Wealth_Index')
    
    def _get_density(self, ins_code: int) -> Optional[float]:
        """Retrieve the density for a given INS code."""
        return self.postal_data_dict.get(ins_code, {}).get('Density')
    
    def enrich_property_data(self) -> pd.DataFrame:
        """
        Enrich property data with INS codes and demographic features.
        
        Returns:
            pd.DataFrame: Enriched property data.
        """
        # Add a new column "INS_Code"
        self.property_data['INS_Code'] = self.property_data['postal_code'].apply(self._get_ins_code)

        # Add demographic features
        self.property_data['Population'] = self.property_data['INS_Code'].apply(self._get_population)
        self.property_data['Wealth_Index'] = self.property_data['INS_Code'].apply(self._get_wealth_index)
        self.property_data['Density'] = self.property_data['INS_Code'].apply(self._get_density)

        return self.property_data

    def save_enriched_data(self, output_path: str) -> None:
        """
        Save the enriched property data to a CSV file.
        
        Args:
            output_path (str): Path to save the enriched dataset.
        """
        self.property_data.to_csv(output_path, index=False)


class PostalCodeFormatter:
    """Class for cleaning and formatting postal codes in a dataset."""

    @staticmethod
    def format_postal_codes(df: pd.DataFrame, postal_code_column: str) -> pd.DataFrame:
        """
        Format and clean postal codes in the dataset.

        Args:
            df (pd.DataFrame): Input DataFrame containing postal code data.
            postal_code_column (str): Name of the column containing postal codes.

        Returns:
            pd.DataFrame: DataFrame with formatted postal codes.
        """
        df[postal_code_column] = df[postal_code_column].apply(
            lambda x: int(x.split(",")[0].strip()) if isinstance(x, str) else (
                int(x) if isinstance(x, (int, float)) and not np.isnan(x) else np.nan
            )
        )
        return df

    @staticmethod
    def save_formatted_data(df: pd.DataFrame, output_path: str) -> None:
        """
        Save the formatted dataset to a CSV file.

        Args:
            df (pd.DataFrame): DataFrame with formatted postal codes.
            output_path (str): Path to save the formatted dataset.
        """
        df.to_csv(output_path, index=False)


class PropertyDataMerger:
    """Class for merging property data with additional demographic and name-based data."""
    
    @staticmethod
    def merge_with_top_names(properties_path: str, names_path: str, output_path: str) -> None:
        """
        Merge property data with the top names and save the resulting DataFrame.

        Args:
            properties_path (str): Path to the CSV file containing property data.
            names_path (str): Path to the CSV file containing names data.
            output_path (str): Path to save the merged dataset.
        """
        # Load datasets
        df_properties = pd.read_csv(properties_path)
        df_new_data = pd.read_csv(names_path)

        # Get top names for each postal code
        top_names = (
            df_new_data.groupby("postal_code")
            .apply(lambda group: group.nlargest(5, "MS_FREQUENCY")[["postal_code", "TX_FST_NAME", "MS_FREQUENCY"]])
            .reset_index(drop=True)
        )

        # Concatenate names and frequencies into a single text column
        top_names_pivot = (
            top_names.groupby("postal_code")
            .apply(lambda group: ", ".join(f"{row['TX_FST_NAME']} ({row['MS_FREQUENCY']})" for _, row in group.iterrows()))
            .reset_index(name="top_names")
        )

        # Merge with property data
        merged_properties = df_properties.merge(top_names_pivot, on="postal_code", how="left")

        # Save the merged dataset
        merged_properties.to_csv(output_path, index=False)


if __name__ == "__main__":
    # Step 1: Enrich property data with demographic features
    processor = PostalDataProcessor(
        property_data_path="./Becode-Bouman-8/projects/immo_eliza/Step_1_Pre_Dataset.csv",
        postal_data_path="./Becode-Bouman-8/projects/immo_eliza/Step_1_Postal_Data.xlsx",
        ins_to_postal_path="./Becode-Bouman-8/projects/immo_eliza/Step_0_Code_INS_to_Postal.json"
    )
    enriched_data = processor.enrich_property_data()
    processor.save_enriched_data("Step_2_Dataset.csv")

    # Step 2: Format postal codes in names data
    df_names = pd.read_csv("/home/batman/Documents/Becode-Bouman-8/names.csv")
    formatted_names = PostalCodeFormatter.format_postal_codes(df_names, postal_code_column="postal_code")
    PostalCodeFormatter.save_formatted_data(formatted_names, "names.csv")

    # Step 3: Merge property data with top names data
    PropertyDataMerger.merge_with_top_names(
        properties_path="Step_2_Dataset.csv",
        names_path="names.csv",
        output_path="Propertities.csv"
    )
