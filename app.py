from flask import Flask, render_template, request, jsonify
from carbon_footprint_model import CarbonFootprintCalculator

app = Flask(__name__)
calculator = CarbonFootprintCalculator()

# Consumption values mapping for each category and level
CONSUMPTION_VALUES = {
    'electricity': {
        'high': 450,      # kWh per month
        'moderate': 300,  # kWh per month
        'low': 150        # kWh per month
    },
    'transport': {
        'high': 350,      # km per week
        'moderate': 200,  # km per week
        'low': 50         # km per week
    },
    'meat': {
        'high': 2.5,      # kg per week
        'moderate': 1.5,  # kg per week
        'low': 0.3        # kg per week
    },
    'waste': {
        'high': 12,       # kg per week
        'moderate': 5,    # kg per week
        'low': 2          # kg per week
    },
    'water': {
        'high': 250,      # liters per day
        'moderate': 150,  # liters per day
        'low': 70         # liters per day
    }
}

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate carbon footprint based on form data."""
    try:
        # Get form data (now dropdown values instead of numbers)
        electricity_level = request.form.get('electricity', 'moderate')
        transport_level = request.form.get('transport', 'moderate')
        meat_level = request.form.get('meat', 'moderate')
        waste_level = request.form.get('waste', 'moderate')
        water_level = request.form.get('water', 'moderate')
        region = request.form.get('region', '')
        
        # Convert levels to numeric values using the mapping
        electricity = CONSUMPTION_VALUES['electricity'][electricity_level]
        transport = CONSUMPTION_VALUES['transport'][transport_level]
        meat = CONSUMPTION_VALUES['meat'][meat_level]
        waste = CONSUMPTION_VALUES['waste'][waste_level]
        water = CONSUMPTION_VALUES['water'][water_level]
        
        # Calculate footprint
        result = calculator.calculate_footprint(electricity, transport, meat, waste, water)
        
        # Add the selected levels to the result
        result['selected_levels'] = {
            'electricity': electricity_level,
            'transport': transport_level,
            'meat': meat_level,
            'waste': waste_level,
            'water': water_level
        }
        
        # Get total footprint and level
        total = result['footprints']['total']
        level = calculator.get_footprint_level(total)
        
        # Get regional comparison if provided
        regional_comparison = ""
        if region:
            regional_comparison = calculator.compare_with_region(total, region)
        
        # Format recommendations
        recommendations = {}
        if result['detailed_recommendations']:
            for category, suggestions in result['detailed_recommendations'].items():
                recommendations[category] = suggestions[:3]  # Limit to top 3 recommendations
        
        # Prepare response data
        response_data = {
            'success': True,
            'footprints': result['footprints'],
            'comparisons': result['comparisons'],
            'level': level,
            'recommendations': recommendations,
            'regional_comparison': regional_comparison,
            'global_averages': result['global_averages'],
            'selected_levels': result['selected_levels']
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/regions', methods=['GET'])
def get_regions():
    """Return a list of valid regions."""
    regions = list(calculator.regional_averages.keys())
    return jsonify(regions)

if __name__ == '__main__':
    app.run(debug=True) 