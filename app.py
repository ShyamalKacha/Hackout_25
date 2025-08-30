#!/usr/bin/env python3
"""
Green Hydrogen Infrastructure Dashboard - FIXED VERSION
Frontend application with mapping and optimization
"""

import json
import math
import random
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load the realistic global hydrogen infrastructure data
def load_hydrogen_data():
    try:
        with open('realistic_global_hydrogen_infrastructure_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Generate sample data if file doesn't exist
        logger.warning("Realistic data file not found, generating sample data...")
        return generate_sample_realistic_data()

def generate_sample_realistic_data():
    """Generate sample realistic data if JSON file is not available"""
    data = {
        "metadata": {
            "created_date": datetime.now().isoformat(),
            "version": "1.0",
            "description": "Sample Realistic Global Green Hydrogen Infrastructure Data",
            "coverage": "Worldwide"
        },
        "renewable_energy": [],
        "hydrogen_production": [],
        "storage_facilities": [],
        "transport_infrastructure": [],
        "demand_centers": [],
        "environmental_constraints": [],
        "economic_data": []
    }
    
    # Generate sample data for all categories with realistic locations
    countries = ["USA", "Germany", "China", "Japan", "Australia", "Brazil", "India", "Saudi Arabia"]
    regions = ["North America", "Europe", "Asia", "South America", "Oceania", "Middle East"]
    
    # Generate sample renewable energy sites
    for i in range(60):
        country = random.choice(countries)
        lat = random.uniform(25, 50) if country == "USA" else random.uniform(-40, 60)
        lon = random.uniform(-125, -65) if country == "USA" else random.uniform(-20, 150)
        data["renewable_energy"].append({
            "id": f"re_{i+1:03d}",
            "name": f"{country} Solar Farm {i+1}",
            "type": "solar" if i % 3 == 0 else "wind" if i % 3 == 1 else "hydro",
            "latitude": lat,
            "longitude": lon,
            "country": country,
            "region": random.choice(regions),
            "capacity_mw": round(random.uniform(50, 1000), 2),
            "capacity_factor": round(random.uniform(0.15, 0.40), 3)
        })
    
    # Generate sample hydrogen production facilities
    for i in range(55):
        country = random.choice(countries)
        lat = random.uniform(25, 50) if country == "USA" else random.uniform(-40, 60)
        lon = random.uniform(-125, -65) if country == "USA" else random.uniform(-20, 150)
        data["hydrogen_production"].append({
            "id": f"hp_{i+1:03d}",
            "name": f"{country} H2 Plant {i+1}",
            "technology": "electrolysis" if i % 2 == 0 else "steam_methane_reforming",
            "latitude": lat,
            "longitude": lon,
            "country": country,
            "region": random.choice(regions),
            "capacity_tpd": round(random.uniform(10, 500), 2),
            "status": random.choice(["operational", "under_construction", "planned"])
        })
    
    # Generate sample storage facilities
    for i in range(52):
        country = random.choice(countries)
        lat = random.uniform(25, 50) if country == "USA" else random.uniform(-40, 60)
        lon = random.uniform(-125, -65) if country == "USA" else random.uniform(-20, 150)
        data["storage_facilities"].append({
            "id": f"st_{i+1:03d}",
            "name": f"{country} Storage Hub {i+1}",
            "type": "underground_salt_cavern" if i % 2 == 0 else "above_ground_tank",
            "latitude": lat,
            "longitude": lon,
            "country": country,
            "region": random.choice(regions),
            "capacity_tons": round(random.uniform(1000, 50000), 2),
            "status": random.choice(["operational", "under_construction", "planned"])
        })
    
    # Generate sample demand centers
    for i in range(58):
        country = random.choice(countries)
        lat = random.uniform(25, 50) if country == "USA" else random.uniform(-40, 60)
        lon = random.uniform(-125, -65) if country == "USA" else random.uniform(-20, 150)
        data["demand_centers"].append({
            "id": f"dc_{i+1:03d}",
            "name": f"{country} Industrial Center {i+1}",
            "sector": "steel" if i % 4 == 0 else "chemical" if i % 4 == 1 else "refining" if i % 4 == 2 else "transport",
            "latitude": lat,
            "longitude": lon,
            "country": country,
            "region": random.choice(regions),
            "annual_demand_tons": round(random.uniform(1000, 20000), 2)
        })
    
    # Generate sample transport infrastructure
    for i in range(62):
        country = random.choice(countries)
        start_lat = random.uniform(25, 50) if country == "USA" else random.uniform(-40, 60)
        start_lon = random.uniform(-125, -65) if country == "USA" else random.uniform(-20, 150)
        distance = random.uniform(100, 1000)
        angle = random.uniform(0, 2 * math.pi)
        end_lat = start_lat + (distance / 111.0) * math.cos(angle)
        end_lon = start_lon + (distance / 111.0) * math.sin(angle) / math.cos(math.radians(start_lat))
        
        data["transport_infrastructure"].append({
            "id": f"tr_{i+1:03d}",
            "name": f"{country} Pipeline {i+1}",
            "mode": "pipeline" if i % 2 == 0 else "truck",
            "start_latitude": round(start_lat, 6),
            "start_longitude": round(start_lon, 6),
            "end_latitude": round(end_lat, 6),
            "end_longitude": round(end_lon, 6),
            "country": country,
            "region": random.choice(regions),
            "distance_km": round(distance, 2),
            "capacity_tpd": round(random.uniform(50, 1000), 2)
        })
    
    # Generate sample environmental constraints
    for i in range(51):
        country = random.choice(countries)
        center_lat = random.uniform(25, 50) if country == "USA" else random.uniform(-40, 60)
        center_lon = random.uniform(-125, -65) if country == "USA" else random.uniform(-20, 150)
        data["environmental_constraints"].append({
            "id": f"ec_{i+1:03d}",
            "name": f"{country} Protected Area {i+1}",
            "type": "national_park" if i % 2 == 0 else "wildlife_reserve",
            "latitude": round(center_lat, 6),
            "longitude": round(center_lon, 6),
            "country": country,
            "region": random.choice(regions),
            "area_hectares": round(random.uniform(1000, 50000), 2),
            "restriction_level": random.choice(["light", "moderate", "strict"])
        })
    
    return data

# Global data variable
HYDROGEN_DATA = load_hydrogen_data()

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat/2) * math.sin(dLat/2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon/2) * math.sin(dLon/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def optimize_location(user_preferences):
    """Optimize location based on user preferences - FIXED VERSION"""
    try:
        # Extract user preferences
        preferred_technology = user_preferences.get('technology', 'electrolysis')
        min_capacity = float(user_preferences.get('min_capacity', 0))
        max_distance_to_renewable = float(user_preferences.get('max_distance_to_renewable', 100))
        min_demand_proximity = float(user_preferences.get('min_demand_proximity', 10))
        budget = float(user_preferences.get('budget', 10000000))
        selected_region = user_preferences.get('region', 'global')
        
        logger.info(f"Optimization parameters: tech={preferred_technology}, min_cap={min_capacity}, region={selected_region}")
        
        # Filter renewable energy sites based on technology, capacity, and region
        suitable_renewables = []
        for site in HYDROGEN_DATA.get('renewable_energy', []):
            # Check region if not global
            if selected_region != 'global' and selected_region != '' and site.get('region', '').lower() != selected_region.lower():
                continue
                
            # Check technology (convert to renewable type)
            renewable_type = preferred_technology.split('_')[0] if '_' in preferred_technology else preferred_technology
            if renewable_type == 'electrolysis':
                renewable_type = 'solar'  # Default to solar for electrolysis
            
            if (site.get('type', '').lower() == renewable_type.lower() or 
                renewable_type in ['electrolysis', 'any', '']) or \
               (renewable_type == 'solar' and site.get('type', '').lower() in ['solar', 'photovoltaic']):
                if site.get('capacity_mw', 0) >= min_capacity:
                    suitable_renewables.append(site)
        
        logger.info(f"Found {len(suitable_renewables)} suitable renewable sites")
        
        if not suitable_renewables:
            # Try with more relaxed criteria
            suitable_renewables = []
            for site in HYDROGEN_DATA.get('renewable_energy', []):
                if selected_region != 'global' and selected_region != '' and site.get('region', '').lower() != selected_region.lower():
                    continue
                if site.get('capacity_mw', 0) >= min_capacity:
                    suitable_renewables.append(site)
            
            if not suitable_renewables:
                # Last resort: all renewable sites
                suitable_renewables = HYDROGEN_DATA.get('renewable_energy', [])[:10]  # Take first 10
                logger.info("Using fallback: first 10 renewable sites")
        
        if not suitable_renewables:
            return {"error": "No suitable renewable energy sites found with given criteria"}
        
        # Find optimal location
        best_score = -1
        best_location = None
        results_considered = 0
        
        # Generate potential locations around suitable renewables
        for renewable in suitable_renewables[:20]:  # Limit to first 20 to avoid timeout
            re_lat = renewable['latitude']
            re_lon = renewable['longitude']
            
            # Generate points around the renewable site
            for i in range(-2, 3):
                for j in range(-2, 3):
                    # Create potential site location
                    site_lat = re_lat + i * 0.5
                    site_lon = re_lon + j * 0.5
                    
                    # Ensure coordinates are valid
                    site_lat = max(-85, min(85, site_lat))
                    site_lon = max(-180, min(180, site_lon))
                    
                    # Check distance to renewable source
                    distance_to_renewable = calculate_distance(
                        re_lat, re_lon, site_lat, site_lon
                    )
                    
                    if distance_to_renewable > max_distance_to_renewable and max_distance_to_renewable > 1:
                        continue
                    
                    # Calculate proximity to demand centers
                    total_demand_proximity = 0
                    demand_count = 0
                    for demand in HYDROGEN_DATA.get('demand_centers', []):
                        # Filter by region if specified
                        if selected_region != 'global' and selected_region != '' and demand.get('region', '').lower() != selected_region.lower():
                            continue
                            
                        distance_to_demand = calculate_distance(
                            site_lat, site_lon, 
                            demand['latitude'], demand['longitude']
                        )
                        # Weight by demand size - avoid division by zero
                        if distance_to_demand > 0:
                            total_demand_proximity += demand['annual_demand_tons'] / (distance_to_demand + 1)
                        else:
                            total_demand_proximity += demand['annual_demand_tons']
                        demand_count += 1
                    
                    avg_demand_proximity = total_demand_proximity / (demand_count if demand_count > 0 else 1)
                    
                    # Skip if below minimum demand proximity (unless it's very low)
                    if avg_demand_proximity < min_demand_proximity and min_demand_proximity > 1:
                        continue
                    
                    # Calculate score (higher is better)
                    score = (
                        (1 / (distance_to_renewable + 1)) * 0.3 +  # Proximity to renewable
                        avg_demand_proximity * 0.5 +  # Proximity to demand
                        (renewable['capacity_mw'] / 10000) * 0.2  # Renewable capacity (normalized)
                    )
                    
                    results_considered += 1
                    if score > best_score:
                        best_score = score
                        best_location = {
                            "latitude": site_lat,
                            "longitude": site_lon,
                            "score": round(score, 4),
                            "distance_to_renewable_km": round(distance_to_renewable, 2),
                            "renewable_source": renewable['name'],
                            "renewable_type": renewable['type'],
                            "renewable_capacity_mw": renewable['capacity_mw'],
                            "avg_demand_proximity_score": round(avg_demand_proximity, 2),
                            "country": renewable.get('country', 'Unknown'),
                            "region": renewable.get('region', 'Unknown')
                        }
        
        logger.info(f"Considered {results_considered} potential locations, best score: {best_score}")
        
        if best_location and best_score > 0:
            return {
                "optimal_location": best_location,
                "message": "Optimal location found based on your criteria"
            }
        else:
            # Return a fallback location if nothing found
            if suitable_renewables:
                fallback_renewable = suitable_renewables[0]
                return {
                    "optimal_location": {
                        "latitude": fallback_renewable['latitude'],
                        "longitude": fallback_renewable['longitude'],
                        "score": 0.1,
                        "distance_to_renewable_km": 0,
                        "renewable_source": fallback_renewable['name'],
                        "renewable_type": fallback_renewable['type'],
                        "renewable_capacity_mw": fallback_renewable['capacity_mw'],
                        "avg_demand_proximity_score": 50,
                        "country": fallback_renewable.get('country', 'Unknown'),
                        "region": fallback_renewable.get('region', 'Unknown')
                    },
                    "message": "Fallback location provided - try relaxing your criteria"
                }
            else:
                return {"error": "No suitable location found with given criteria"}
            
    except Exception as e:
        logger.error(f"Optimization error: {str(e)}")
        return {"error": f"Optimization failed: {str(e)}"}

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API endpoint to get all hydrogen infrastructure data"""
    return jsonify(HYDROGEN_DATA)

@app.route('/api/optimize', methods=['POST'])
def optimize():
    """API endpoint for location optimization"""
    try:
        user_preferences = request.json
        logger.info(f"Received optimization request: {user_preferences}")
        result = optimize_location(user_preferences)
        logger.info(f"Optimization result: {result}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({"error": "Optimization request failed"}), 500

@app.route('/api/categories')
def get_categories():
    """API endpoint to get data categories"""
    categories = [key for key in HYDROGEN_DATA.keys() if key != 'metadata']
    return jsonify(categories)

@app.route('/api/regions')
def get_regions():
    """API endpoint to get available regions"""
    regions = set()
    for category in ['renewable_energy', 'hydrogen_production', 'demand_centers']:
        if category in HYDROGEN_DATA:
            for item in HYDROGEN_DATA[category]:
                if 'region' in item:
                    regions.add(item['region'])
    return jsonify(sorted(list(regions)))

@app.route('/api/debug/data_info')
def debug_data_info():
    """Debug endpoint to check data structure"""
    info = {
        "total_renewable_sites": len(HYDROGEN_DATA.get('renewable_energy', [])),
        "regions": list(set(site.get('region', 'Unknown') for site in HYDROGEN_DATA.get('renewable_energy', []))),
        "technologies": list(set(site.get('type', 'Unknown') for site in HYDROGEN_DATA.get('renewable_energy', []))),
        "capacity_range": {
            "min": min(site.get('capacity_mw', 0) for site in HYDROGEN_DATA.get('renewable_energy', [])) if HYDROGEN_DATA.get('renewable_energy') else 0,
            "max": max(site.get('capacity_mw', 0) for site in HYDROGEN_DATA.get('renewable_energy', [])) if HYDROGEN_DATA.get('renewable_energy') else 0
        }
    }
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)