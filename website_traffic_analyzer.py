import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random
from collections import defaultdict

class WebsiteTrafficAnalyzer:
    def __init__(self, data_file=None):
        """Initialize the website traffic analyzer with optional data file."""
        self.data = None
        self.data_file = data_file
        
    def load_data(self):
        """Load data from CSV file if available."""
        try:
            self.data = pd.read_csv(self.data_file)
            print(f"Data loaded successfully from {self.data_file}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
            
    def generate_sample_data(self, days=30):
        """Generate synthetic website traffic data for analysis."""
        print("Generating sample website traffic data...")
        
        # Set seed for reproducibility
        np.random.seed(42)
        
        # Create date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        date_range = [start_date + timedelta(days=i) for i in range(days)]
        
        # Data structures
        records = []
        
        # Pages to simulate
        pages = [
            '/home', '/products', '/about', '/contact', '/blog', 
            '/pricing', '/signup', '/login', '/support', '/faq'
        ]
        
        # Traffic sources
        sources = [
            'Google', 'Direct', 'Facebook', 'Twitter', 'Email', 
            'LinkedIn', 'Bing', 'Instagram', 'Referral', 'Other'
        ]
        
        # Devices
        devices = ['Desktop', 'Mobile', 'Tablet']
        
        # Countries
        countries = [
            'United States', 'United Kingdom', 'Canada', 'Germany', 
            'France', 'Australia', 'India', 'Japan', 'Brazil', 'Mexico'
        ]
        
        # User IDs (reusing some to simulate returning visitors)
        user_ids = [f"user_{i}" for i in range(1, 1001)]
        
        # Generate hourly data for more realistic patterns
        for date in date_range:
            # Create daily pattern with peaks during business hours
            for hour in range(24):
                # More traffic during business hours
                if 9 <= hour <= 17:
                    visits_factor = 1.5
                elif 18 <= hour <= 22:
                    visits_factor = 1.2
                else:
                    visits_factor = 0.5
                    
                # Weekends have different patterns
                if date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                    visits_factor *= 0.7
                
                # Number of visits in this hour
                num_visits = int(np.random.poisson(20 * visits_factor))
                
                for _ in range(num_visits):
                    # Create session
                    user_id = np.random.choice(user_ids)
                    session_id = f"session_{date.strftime('%Y%m%d')}_{hour}_{np.random.randint(1000, 9999)}"
                    session_start = date.replace(hour=hour, minute=np.random.randint(0, 60))
                    source = np.random.choice(sources, p=[0.4, 0.2, 0.15, 0.05, 0.05, 0.05, 0.03, 0.03, 0.02, 0.02])
                    device = np.random.choice(devices, p=[0.55, 0.35, 0.1])
                    country = np.random.choice(countries, p=[0.45, 0.15, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.03, 0.02])
                    
                    # Number of pages in this session (some are bounces)
                    num_pages = np.random.choice([1, 2, 3, 4, 5, 6], p=[0.3, 0.25, 0.2, 0.15, 0.05, 0.05])
                    is_bounce = (num_pages == 1)
                    
                    # First page is often homepage for new visits
                    if source != 'Direct' and np.random.random() < 0.7:
                        first_page = '/home'
                    else:
                        first_page = np.random.choice(pages)
                    
                    # Track conversion (signup or purchase)
                    converted = False
                    
                    # Add session pages
                    viewed_pages = []
                    for i in range(num_pages):
                        if i == 0:
                            page = first_page
                        else:
                            # Subsequent pages depend somewhat on previous page
                            if viewed_pages[-1] == '/products' and np.random.random() < 0.4:
                                page = '/signup'
                            elif viewed_pages[-1] == '/pricing' and np.random.random() < 0.3:
                                page = '/signup'
                            else:
                                page = np.random.choice([p for p in pages if p not in viewed_pages][:5] if viewed_pages else pages)
                        
                        viewed_pages.append(page)
                        
                        # Time on page varies
                        if i < num_pages - 1:  # Not the last page
                            time_on_page = int(np.random.gamma(shape=2.0, scale=30.0))  # seconds
                        else:
                            time_on_page = 0  # Last page has no time recorded
                        
                        # Check for conversion
                        if page == '/signup' and np.random.random() < 0.2:
                            converted = True
                        
                        timestamp = session_start + timedelta(minutes=i*2)  # Pages viewed every ~2 minutes
                        
                        records.append({
                            'timestamp': timestamp,
                            'date': timestamp.date(),
                            'hour': timestamp.hour,
                            'user_id': user_id,
                            'session_id': session_id,
                            'page': page,
                            'time_on_page': time_on_page,
                            'source': source,
                            'device': device,
                            'country': country,
                            'is_bounce': is_bounce,
                            'converted': converted
                        })
        
        # Convert to DataFrame
        self.data = pd.DataFrame(records)
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data['date'] = pd.to_datetime(self.data['date'])
        
        print(f"Generated {len(self.data)} page views across {days} days")
        return self.data
    
    def save_data(self, filename="website_traffic_data.csv"):
        """Save the data to a CSV file."""
        if self.data is not None:
            self.data.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        else:
            print("No data to save")
    
    def basic_metrics(self):
        """Calculate and display basic website traffic metrics."""
        if self.data is None:
            print("No data available. Please load or generate data first.")
            return
            
        print("\n=== Basic Website Traffic Metrics ===")
        
        # Total pageviews and unique visitors
        total_pageviews = len(self.data)
        unique_visitors = self.data['user_id'].nunique()
        unique_sessions = self.data['session_id'].nunique()
        
        # Calculate sessions per visitor
        sessions_per_visitor = unique_sessions / unique_visitors
        
        # Calculate bounce rate
        bounce_sessions = self.data.drop_duplicates('session_id')['is_bounce'].sum()
        bounce_rate = bounce_sessions / unique_sessions * 100
        
        # Calculate conversion rate
        converted_sessions = self.data.groupby('session_id')['converted'].max().sum()
        conversion_rate = converted_sessions / unique_sessions * 100
        
        # Pages per session
        pages_per_session = total_pageviews / unique_sessions
        
        # Calculate average time on site
        session_durations = self.data.groupby('session_id')['time_on_page'].sum()
        avg_session_duration = session_durations.mean()
        
        # Print metrics
        print(f"Total Pageviews: {total_pageviews:,}")
        print(f"Unique Visitors: {unique_visitors:,}")
        print(f"Total Sessions: {unique_sessions:,}")
        print(f"Pages per Session: {pages_per_session:.2f}")
        print(f"Sessions per Visitor: {sessions_per_visitor:.2f}")
        print(f"Bounce Rate: {bounce_rate:.2f}%")
        print(f"Conversion Rate: {conversion_rate:.2f}%")
        print(f"Average Session Duration: {avg_session_duration:.0f} seconds")
        
        return {
            'total_pageviews': total_pageviews,
            'unique_visitors': unique_visitors,
            'unique_sessions': unique_sessions,
            'pages_per_session': pages_per_session,
            'sessions_per_visitor': sessions_per_visitor,
            'bounce_rate': bounce_rate,
            'conversion_rate': conversion_rate,
            'avg_session_duration': avg_session_duration
        }
    
    def traffic_over_time(self, time_unit='day'):
        """Analyze and visualize traffic patterns over time."""
        if self.data is None:
            print("No data available. Please load or generate data first.")
            return
            
        plt.figure(figsize=(12, 6))
        
        if time_unit == 'day':
            # Daily traffic
            daily_traffic = self.data.groupby(self.data['date'])['session_id'].nunique()
            daily_traffic.plot(kind='line', marker='o')
            plt.title('Daily Sessions')
            plt.xlabel('Date')
            plt.ylabel('Number of Sessions')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
            
        elif time_unit == 'hour':
            # Hourly patterns
            hourly_traffic = self.data.groupby('hour')['session_id'].nunique()
            hourly_traffic.plot(kind='bar')
            plt.title('Hourly Traffic Pattern')
            plt.xlabel('Hour of Day')
            plt.ylabel('Number of Sessions')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
            
        elif time_unit == 'day_of_week':
            # Day of week patterns
            self.data['day_of_week'] = self.data['timestamp'].dt.day_name()
            order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_traffic = self.data.groupby('day_of_week')['session_id'].nunique().reindex(order)
            day_traffic.plot(kind='bar')
            plt.title('Traffic by Day of Week')
            plt.xlabel('Day of Week')
            plt.ylabel('Number of Sessions')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
    
    def analyze_traffic_sources(self):
        """Analyze and visualize traffic sources."""
        if self.data is None:
            print("No data available. Please load or generate data first.")
            return
            
        # Get sessions by source
        source_counts = self.data.drop_duplicates('session_id')['source'].value_counts()
        
        # Calculate bounce rates by source
        source_sessions = self.data.drop_duplicates('session_id').groupby('source')['is_bounce'].count()
        source_bounces = self.data.drop_duplicates('session_id').groupby('source')['is_bounce'].sum()
        source_bounce_rates = (source_bounces / source_sessions * 100).sort_values(ascending=False)
        
        # Calculate conversion rates by source
        source_conversions = self.data.drop_duplicates('session_id').groupby('source')['converted'].sum()
        source_conversion_rates = (source_conversions / source_sessions * 100).sort_values(ascending=False)
        
        # Plot traffic sources
        plt.figure(figsize=(10, 6))
        source_counts.plot(kind='bar')
        plt.title('Sessions by Traffic Source')
        plt.xlabel('Traffic Source')
        plt.ylabel('Number of Sessions')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Plot bounce rates by source
        plt.figure(figsize=(10, 6))
        source_bounce_rates.plot(kind='bar')
        plt.title('Bounce Rate by Traffic Source')
        plt.xlabel('Traffic Source')
        plt.ylabel('Bounce Rate (%)')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Plot conversion rates by source
        plt.figure(figsize=(10, 6))
        source_conversion_rates.plot(kind='bar')
        plt.title('Conversion Rate by Traffic Source')
        plt.xlabel('Traffic Source')
        plt.ylabel('Conversion Rate (%)')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Print summary
        print("\n=== Traffic Source Analysis ===")
        
        summary_df = pd.DataFrame({
            'Sessions': source_counts,
            'Bounce Rate (%)': source_bounce_rates,
            'Conversion Rate (%)': source_conversion_rates
        }).fillna(0).sort_values('Sessions', ascending=False)
        
        print(summary_df.round(2))
        return summary_df
    
    def popular_pages(self):
        """Analyze and visualize the most popular pages."""
        if self.data is None:
            print("No data available. Please load or generate data first.")
            return
            
        # Count pageviews
        page_views = self.data['page'].value_counts()
        
        # Calculate time on page
        page_time = self.data.groupby('page')['time_on_page'].mean().sort_values(ascending=False)
        
        # Calculate exit rates (percentage of exits from each page)
        # First identify exit pages (last page in each session)
        session_pages = self.data.sort_values(['session_id', 'timestamp'])
        last_pages = session_pages.groupby('session_id').last()
        exit_counts = last_pages['page'].value_counts()
        
        # Calculate exit rate
        exit_rates = pd.DataFrame({
            'Exits': exit_counts,
            'Pageviews': page_views
        }).fillna(0)
        exit_rates['Exit Rate (%)'] = (exit_rates['Exits'] / exit_rates['Pageviews'] * 100).round(2)
        
        # Plot popular pages
        plt.figure(figsize=(10, 6))
        page_views.head(10).plot(kind='bar')
        plt.title('Most Popular Pages')
        plt.xlabel('Page')
        plt.ylabel('Number of Pageviews')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Plot average time on page
        plt.figure(figsize=(10, 6))
        page_time.head(10).plot(kind='bar')
        plt.title('Average Time on Page')