from carbon_footprint_model import CarbonFootprintCalculator
import sys
import os

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(text.center(60))
    print("=" * 60)

def print_section(text):
    """Print a formatted section header."""
    print("\n" + "-" * 50)
    print(text)
    print("-" * 50)

def get_float_input(prompt, default=None):
    """Get a float input with validation and default value."""
    while True:
        try:
            value_str = input(prompt)
            if value_str.strip() == "" and default is not None:
                return default
            return float(value_str)
        except ValueError:
            print("Please enter a valid number.")

def main():
    clear_screen()
    print_header("Carbon Footprint Calculator")
    
    print("\nThis tool calculates your carbon footprint and compares it with global averages.")
    print("It will provide personalized recommendations to help reduce your environmental impact.")
    print("\nPlease provide the following information (or press Enter for default values):")
    
    try:
        # Get user inputs with defaults
        electricity = get_float_input("\nMonthly electricity consumption (kWh) [300]: ", 300)
        transport = get_float_input("Weekly distance traveled by car (km) [200]: ", 200)
        meat = get_float_input("Weekly meat consumption (kg) [1.5]: ", 1.5)
        waste = get_float_input("Weekly non-recycled waste (kg) [5]: ", 5)
        water = get_float_input("Daily water consumption (liters) [150]: ", 150)
        
        # Get region with validation
        valid_regions = ["North America", "Europe", "Asia", "Africa", "South America", "Oceania"]
        print("\nValid regions:", ", ".join(valid_regions))
        region = input("Your region (or press Enter for global comparison only): ")
        if region and region not in valid_regions:
            print(f"Warning: '{region}' is not a recognized region. Using global comparison only.")
            region = ""
        
        # Calculate footprint
        calculator = CarbonFootprintCalculator()
        result = calculator.calculate_footprint(electricity, transport, meat, waste, water)
        
        # Display results
        clear_screen()
        print_header("Your Carbon Footprint Results")
        
        # Display footprint by category
        print_section("Your Annual Carbon Footprint (metric tons CO2)")
        
        for category, value in result['footprints'].items():
            if category != 'total':
                status = result['comparisons'][category]
                status_indicator = ""
                if status == "high":
                    status_indicator = "⚠️ HIGH"
                elif status == "moderate":
                    status_indicator = "⚠️ MODERATE"
                elif status == "low":
                    status_indicator = "✓ LOW"
                
                print(f"- {category.capitalize()}: {value:.2f} tons ({status_indicator})")
                print(f"  Global average: {result['global_averages'][category]:.2f} tons")
                
                # Show comparison as percentage
                percentage = (value / result['global_averages'][category]) * 100
                if percentage > 100:
                    print(f"  You're {percentage - 100:.0f}% above the global average")
                else:
                    print(f"  You're {100 - percentage:.0f}% below the global average")
                print()
        
        # Display total footprint
        total = result['footprints']['total']
        level = calculator.get_footprint_level(total)
        
        print_section("Total Carbon Footprint")
        print(f"Your total: {total:.2f} tons CO2/year")
        print(f"Global average: {result['global_averages']['total']:.2f} tons CO2/year")
        
        # Show comparison as percentage
        percentage = (total / result['global_averages']['total']) * 100
        if percentage > 100:
            print(f"You're {percentage - 100:.0f}% above the global average")
        else:
            print(f"You're {100 - percentage:.0f}% below the global average")
        
        # Compare with regional average if provided
        if region:
            print("\n" + calculator.compare_with_region(total, region))
        
        # Display recommendations for high categories
        if result['detailed_recommendations']:
            print_section("Personalized Recommendations")
            print("Based on your inputs, here are some ways to reduce your carbon footprint:")
            
            for category, suggestions in result['detailed_recommendations'].items():
                print(f"\nFor {category.capitalize()}:")
                for i, suggestion in enumerate(suggestions[:3], 1):
                    print(f"  {i}. {suggestion['title']}")
                    print(f"     {suggestion['description']}")
                    print(f"     Impact: {suggestion['impact']}, Effort: {suggestion['effort']}")
        else:
            print_section("Great Job!")
            print("Your carbon footprint is below or at global averages.")
            print("Keep up the good work and consider these additional steps:")
            print("1. Continue to monitor your consumption patterns")
            print("2. Advocate for climate-friendly policies in your community")
            print("3. Share your sustainable practices with friends and family")
            
    except ValueError:
        print("Error: Please enter valid numerical values.")
    except KeyboardInterrupt:
        print("\nCalculation cancelled.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print("\nThank you for using the Carbon Footprint Calculator!")

if __name__ == "__main__":
    main() 