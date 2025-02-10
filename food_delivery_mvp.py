import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import os
from typing import List, Dict

class FoodDeliveryAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_foodora(self, city: str) -> List[Dict]:
        """Basic scraper for Foodora"""
        vendors = []
        url = f"https://www.foodora.no/en/restaurants/city/{city}"
        
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all restaurant cards
            restaurant_cards = soup.find_all('div', class_='restaurant-card')
            
            for card in restaurant_cards:
                vendor = {
                    'name': card.find('h3').text.strip() if card.find('h3') else 'Unknown',
                    'cuisine': card.find('span', class_='cuisine-type').text.strip() if card.find('span', class_='cuisine-type') else 'Unknown',
                    'price_category': self._extract_price(card),
                    'platform': 'Foodora',
                    'city': city
                }
                vendors.append(vendor)
                
        except Exception as e:
            print(f"Error scraping Foodora for {city}: {str(e)}")
            
        return vendors

    def scrape_wolt(self, city: str) -> List[Dict]:
        """Basic scraper for Wolt"""
        vendors = []
        url = f"https://wolt.com/en/nor/cities/{city}/restaurants"
        
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all venue cards
            venue_cards = soup.find_all('div', attrs={'data-test-id': 'venueCard'})
            
            for card in venue_cards:
                vendor = {
                    'name': card.find('h3').text.strip() if card.find('h3') else 'Unknown',
                    'cuisine': card.find('div', class_='venue-type').text.strip() if card.find('div', class_='venue-type') else 'Unknown',
                    'price_category': self._extract_price(card),
                    'platform': 'Wolt',
                    'city': city
                }
                vendors.append(vendor)
                
        except Exception as e:
            print(f"Error scraping Wolt for {city}: {str(e)}")
            
        return vendors

    def _extract_price(self, card) -> str:
        """Extract price category"""
        try:
            price_element = card.find('div', class_='price-range')
            if price_element:
                price_text = price_element.text.strip()
                return '$' * (price_text.count('€') or 1)
            return '$'
        except:
            return '$'

    def analyze_data(self, city: str) -> Dict:
        """Analyze vendor data for a city"""
        # Scrape data
        foodora_vendors = self.scrape_foodora(city)
        time.sleep(2)  # Be nice to servers
        wolt_vendors = self.scrape_wolt(city)
        
        # Basic analysis
        analysis = {
            'city': city,
            'vendor_counts': {
                'foodora': len(foodora_vendors),
                'wolt': len(wolt_vendors)
            },
            'unique_vendors': {
                'foodora': len(set(v['name'] for v in foodora_vendors)),
                'wolt': len(set(v['name'] for v in wolt_vendors))
            },
            'cuisine_types': {
                'foodora': list(set(v['cuisine'] for v in foodora_vendors)),
                'wolt': list(set(v['cuisine'] for v in wolt_vendors))
            },
            'price_distribution': {
                'foodora': self._calculate_price_distribution(foodora_vendors),
                'wolt': self._calculate_price_distribution(wolt_vendors)
            }
        }
        
        return analysis

    def _calculate_price_distribution(self, vendors: List[Dict]) -> Dict:
        """Calculate price category distribution"""
        total = len(vendors)
        if total == 0:
            return {'$': 0, '$$': 0, '$$$': 0}
            
        distribution = {'$': 0, '$$': 0, '$$$': 0}
        for vendor in vendors:
            price_cat = vendor['price_category']
            if price_cat in distribution:
                distribution[price_cat] += 1
                
        return {k: (v/total)*100 for k, v in distribution.items()}

    def generate_report(self, cities: List[str]) -> Dict:
        """Generate analysis report for multiple cities"""
        report = {
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'cities_analyzed': cities,
            'analysis': {}
        }
        
        for city in cities:
            print(f"Analyzing {city}...")
            report['analysis'][city] = self.analyze_data(city)
            time.sleep(2)  # Be nice to servers
            
        return report

    def save_report(self, report: Dict, filename: str = 'food_delivery_analysis.json'):
        """Save report to JSON file"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {filename}")

def run_analysis():
    """Run the analysis and save results"""
    # Initialize analyzer
    analyzer = FoodDeliveryAnalyzer()
    
    # Define cities to analyze
    cities = ['oslo', 'bergen']  # Starting with just two cities for MVP
    
    # Generate filename with timestamp
    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    filename = f'/app/data/food_delivery_analysis_{timestamp}.json'
    
    try:
        # Generate and save report
        report = analyzer.generate_report(cities)
        analyzer.save_report(report, filename)
        print(f"Analysis completed successfully at {timestamp}")
    except Exception as e:
        print(f"Error running analysis: {str(e)}")

def main():
    # Check if running in scheduled mode
    schedule_interval = os.getenv('SCHEDULE_INTERVAL')
    
    if schedule_interval:
        # Run on a schedule
        import schedule
        interval = int(schedule_interval)
        
        print(f"Starting scheduled runs every {interval} hours")
        schedule.every(interval).hours.do(run_analysis)
        
        # Run once immediately
        run_analysis()
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        # Run once
        run_analysis()

if __name__ == "__main__":
    main()