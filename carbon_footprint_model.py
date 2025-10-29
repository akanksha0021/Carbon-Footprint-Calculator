import pandas as pd
import numpy as np
from carbon_footprint_data import GLOBAL_AVERAGES, REGIONAL_AVERAGES, EMISSION_FACTORS, REDUCTION_SUGGESTIONS

class CarbonFootprintCalculator:
    def __init__(self):
        # Use data from the imported dataset
        self.global_averages = GLOBAL_AVERAGES
        self.regional_averages = {region: data['total'] for region, data in REGIONAL_AVERAGES.items()}
        self.emission_factors = EMISSION_FACTORS
        self.suggestions = {category: [item['title'] for item in suggestions] 
                           for category, suggestions in REDUCTION_SUGGESTIONS.items()}
        self.detailed_suggestions = REDUCTION_SUGGESTIONS
    
    def calculate_footprint(self, electricity_kwh, transport_km, meat_consumption, 
                           waste_kg, water_liters):
        """
        Calculate carbon footprint based on user inputs
        
        Parameters:
        electricity_kwh: Monthly electricity consumption in kWh
        transport_km: Weekly distance traveled by car in km
        meat_consumption: Weekly meat consumption in kg
        waste_kg: Weekly non-recycled waste in kg
        water_liters: Daily water consumption in liters
        
        Returns:
        Dictionary with carbon footprint values and comparisons
        """
        # Convert inputs to annual carbon footprint (metric tons CO2)
        electricity_footprint = electricity_kwh * 12 * self.emission_factors['electricity']['mixed_grid']
        transport_footprint = transport_km * 52 * self.emission_factors['transportation']['car_petrol']
        food_footprint = meat_consumption * 52 * self.emission_factors['food']['beef']
        waste_footprint = waste_kg * 52 * self.emission_factors['waste']['landfill']
        water_footprint = water_liters * 365 * self.emission_factors['water']['cold_water']
        
        # Calculate total footprint
        total_footprint = (electricity_footprint + transport_footprint + 
                          food_footprint + waste_footprint + water_footprint)
        
        # Create result dictionary
        footprints = {
            'electricity': electricity_footprint,
            'transportation': transport_footprint,
            'food': food_footprint,
            'waste': waste_footprint,
            'water': water_footprint,
            'total': total_footprint
        }
        
        # Compare with global averages
        comparisons = {}
        for category, value in footprints.items():
            if value > self.global_averages[category] * 1.2:
                comparisons[category] = "high"
            elif value < self.global_averages[category] * 0.8:
                comparisons[category] = "low"
            else:
                comparisons[category] = "moderate"
        
        # Generate suggestions for high categories
        recommendations = {}
        detailed_recommendations = {}
        for category, status in comparisons.items():
            if status == "high" and category in self.suggestions:
                recommendations[category] = self.suggestions[category]
                detailed_recommendations[category] = self.detailed_suggestions[category]
        
        return {
            'footprints': footprints,
            'comparisons': comparisons,
            'recommendations': recommendations,
            'detailed_recommendations': detailed_recommendations,
            'global_averages': self.global_averages
        }
    
    def get_footprint_level(self, total_footprint):
        """
        Get overall footprint level compared to global average
        """
        if total_footprint > self.global_averages['total'] * 1.2:
            return "high"
        elif total_footprint < self.global_averages['total'] * 0.8:
            return "low"
        else:
            return "moderate"
    
    def compare_with_region(self, total_footprint, region):
        """
        Compare footprint with regional average
        """
        if region in self.regional_averages:
            regional_avg = self.regional_averages[region]
            if total_footprint > regional_avg * 1.1:
                return f"Your carbon footprint is higher than the {region} average of {regional_avg} tons CO2/year"
            elif total_footprint < regional_avg * 0.9:
                return f"Your carbon footprint is lower than the {region} average of {regional_avg} tons CO2/year"
            else:
                return f"Your carbon footprint is close to the {region} average of {regional_avg} tons CO2/year"
        else:
            return "Region not found in database"
    
    def get_detailed_recommendations(self, category):
        """
        Get detailed recommendations for a specific category
        """
        if category in self.detailed_suggestions:
            return self.detailed_suggestions[category]
        return [] 