"""
Carbon Footprint Calculator Dataset

This file contains detailed data for the carbon footprint calculator,
including emission factors, global and regional averages, and suggestions
for reducing carbon footprint.
"""

# Emission factors for different activities
EMISSION_FACTORS = {
    'electricity': {
        'coal': 0.001, # kg CO2 per kWh
        'natural_gas': 0.0005, # kg CO2 per kWh
        'renewable': 0.00005, # kg CO2 per kWh
        'mixed_grid': 0.0005 # kg CO2 per kWh (average)
    },
    'transportation': {
        'car_petrol': 0.00024, # kg CO2 per km
        'car_diesel': 0.00022, # kg CO2 per km
        'car_electric': 0.00007, # kg CO2 per km
        'bus': 0.00010, # kg CO2 per km per passenger
        'train': 0.00006, # kg CO2 per km per passenger
        'plane_short': 0.00026, # kg CO2 per km per passenger
        'plane_long': 0.00021 # kg CO2 per km per passenger
    },
    'food': {
        'beef': 0.06, # kg CO2 per kg
        'lamb': 0.04, # kg CO2 per kg
        'pork': 0.012, # kg CO2 per kg
        'chicken': 0.007, # kg CO2 per kg
        'fish': 0.005, # kg CO2 per kg
        'dairy': 0.004, # kg CO2 per kg
        'vegetables_local': 0.0005, # kg CO2 per kg
        'vegetables_imported': 0.002, # kg CO2 per kg
        'fruits_local': 0.0007, # kg CO2 per kg
        'fruits_imported': 0.003 # kg CO2 per kg
    },
    'waste': {
        'landfill': 0.0007, # kg CO2 per kg waste
        'recycled': 0.0001, # kg CO2 per kg waste
        'composted': 0.00005 # kg CO2 per kg waste
    },
    'water': {
        'cold_water': 0.000001, # kg CO2 per liter
        'hot_water': 0.000004 # kg CO2 per liter
    }
}

# Global average carbon footprint data (in metric tons of CO2 per year)
GLOBAL_AVERAGES = {
    'electricity': 1.8,  # Average household electricity consumption
    'transportation': 2.5,  # Average transportation emissions
    'food': 1.7,  # Average food-related emissions
    'waste': 0.5,  # Average waste-related emissions
    'water': 0.3,  # Average water-related emissions
    'total': 6.8  # Global average total carbon footprint per person
}

# Regional averages (metric tons CO2 per year per person)
REGIONAL_AVERAGES = {
    'North America': {
        'total': 16.1,
        'electricity': 5.8,
        'transportation': 5.5,
        'food': 3.2,
        'waste': 1.1,
        'water': 0.5
    },
    'Europe': {
        'total': 7.9,
        'electricity': 2.6,
        'transportation': 2.8,
        'food': 1.7,
        'waste': 0.5,
        'water': 0.3
    },
    'Asia': {
        'total': 4.2,
        'electricity': 1.5,
        'transportation': 1.2,
        'food': 1.0,
        'waste': 0.3,
        'water': 0.2
    },
    'Africa': {
        'total': 1.2,
        'electricity': 0.3,
        'transportation': 0.4,
        'food': 0.3,
        'waste': 0.1,
        'water': 0.1
    },
    'South America': {
        'total': 3.8,
        'electricity': 1.1,
        'transportation': 1.3,
        'food': 1.0,
        'waste': 0.2,
        'water': 0.2
    },
    'Oceania': {
        'total': 10.7,
        'electricity': 3.9,
        'transportation': 3.6,
        'food': 2.1,
        'waste': 0.7,
        'water': 0.4
    }
}

# Suggestions for reducing carbon footprint by category
REDUCTION_SUGGESTIONS = {
    'electricity': [
        {
            'title': "Switch to energy-efficient LED bulbs",
            'description': "LED bulbs use up to 80% less energy than traditional incandescent bulbs and last much longer.",
            'impact': "Medium",
            'effort': "Low"
        },
        {
            'title': "Unplug electronics when not in use",
            'description': "Many devices consume power even when turned off (phantom energy). Use power strips to easily cut power.",
            'impact': "Low",
            'effort': "Low"
        },
        {
            'title': "Install solar panels",
            'description': "Generate your own clean electricity and potentially sell excess back to the grid.",
            'impact': "High",
            'effort': "High"
        },
        {
            'title': "Use energy-efficient appliances",
            'description': "Look for Energy Star or equivalent ratings when purchasing new appliances.",
            'impact': "Medium",
            'effort': "Medium"
        },
        {
            'title': "Adjust thermostat settings",
            'description': "Lower heating by 1-2°C in winter and raise cooling by 1-2°C in summer to save significant energy.",
            'impact': "Medium",
            'effort': "Low"
        },
        {
            'title': "Improve home insulation",
            'description': "Better insulation reduces heating and cooling needs dramatically.",
            'impact': "High",
            'effort': "High"
        }
    ],
    'transportation': [
        {
            'title': "Use public transportation",
            'description': "Buses and trains generally have lower emissions per passenger than individual cars.",
            'impact': "Medium",
            'effort': "Medium"
        },
        {
            'title': "Carpool or rideshare",
            'description': "Sharing rides reduces the number of vehicles on the road and splits emissions among passengers.",
            'impact': "Medium",
            'effort': "Low"
        },
        {
            'title': "Walk or bike for short trips",
            'description': "Zero-emission transportation that also improves health.",
            'impact': "Medium",
            'effort': "Medium"
        },
        {
            'title': "Switch to an electric or hybrid vehicle",
            'description': "Electric vehicles produce fewer lifecycle emissions, especially when charged with renewable energy.",
            'impact': "High",
            'effort': "High"
        },
        {
            'title': "Combine errands into fewer trips",
            'description': "Plan ahead to reduce the total distance driven.",
            'impact': "Low",
            'effort': "Low"
        },
        {
            'title': "Work from home when possible",
            'description': "Eliminates commuting emissions entirely on those days.",
            'impact': "Medium",
            'effort': "Variable"
        }
    ],
    'food': [
        {
            'title': "Reduce meat consumption",
            'description': "Especially beef and lamb, which have the highest carbon footprints.",
            'impact': "High",
            'effort': "Medium"
        },
        {
            'title': "Buy local and seasonal produce",
            'description': "Reduces transportation emissions and often uses fewer resources.",
            'impact': "Medium",
            'effort': "Medium"
        },
        {
            'title': "Reduce food waste",
            'description': "Plan meals, store food properly, and use leftovers to minimize waste.",
            'impact': "Medium",
            'effort': "Low"
        },
        {
            'title': "Compost food scraps",
            'description': "Reduces methane emissions from landfills and creates nutrient-rich soil.",
            'impact': "Low",
            'effort': "Low"
        },
        {
            'title': "Grow some of your own food",
            'description': "Even a small garden or some herbs can reduce purchased food emissions.",
            'impact': "Low",
            'effort': "Medium"
        },
        {
            'title': "Choose organic and sustainably produced foods",
            'description': "Often uses fewer synthetic fertilizers and pesticides.",
            'impact': "Low",
            'effort': "Medium"
        }
    ],
    'waste': [
        {
            'title': "Recycle consistently",
            'description': "Learn local recycling rules and follow them carefully to ensure materials actually get recycled.",
            'impact': "Medium",
            'effort': "Low"
        },
        {
            'title': "Use reusable items",
            'description': "Bags, bottles, containers, and other items that replace single-use products.",
            'impact': "Medium",
            'effort': "Low"
        },
        {
            'title': "Buy products with less packaging",
            'description': "Choose bulk items or products with minimal, recyclable packaging.",
            'impact': "Medium",
            'effort': "Medium"
        },
        {
            'title': "Compost organic waste",
            'description': "Keeps organic material out of landfills where it produces methane.",
            'impact': "Medium",
            'effort': "Medium"
        },
        {
            'title': "Repair rather than replace",
            'description': "Extends product life and reduces manufacturing emissions for new products.",
            'impact': "Medium",
            'effort': "Variable"
        },
        {
            'title': "Practice zero-waste shopping",
            'description': "Bring your own containers to stores that allow refilling.",
            'impact': "Medium",
            'effort': "High"
        }
    ],
    'water': [
        {
            'title': "Take shorter showers",
            'description': "Reduces both water usage and the energy needed to heat it.",
            'impact': "Low",
            'effort': "Low"
        },
        {
            'title': "Fix leaks promptly",
            'description': "Even small leaks can waste thousands of liters annually.",
            'impact': "Low",
            'effort': "Variable"
        },
        {
            'title': "Install water-efficient fixtures",
            'description': "Low-flow showerheads, faucet aerators, and efficient toilets.",
            'impact': "Medium",
            'effort': "Medium"
        },
        {
            'title': "Collect rainwater for garden use",
            'description': "Reduces treated water usage for plants.",
            'impact': "Low",
            'effort': "Medium"
        },
        {
            'title': "Run full loads of laundry and dishes",
            'description': "Maximizes efficiency of water and energy use.",
            'impact': "Low",
            'effort': "Low"
        },
        {
            'title': "Choose drought-resistant landscaping",
            'description': "Reduces or eliminates the need for irrigation.",
            'impact': "Medium",
            'effort': "High"
        }
    ]
} 