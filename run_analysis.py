from website_traffic_analyzer import WebsiteTrafficAnalyzer

# Create analyzer instance
analyzer = WebsiteTrafficAnalyzer()

# Generate sample data
analyzer.generate_sample_data(days=30)

# Save data to CSV (optional)
analyzer.save_data("website_traffic_data.csv")

# Run basic analysis
analyzer.basic_metrics()

# Visualize traffic over time
print("\nAnalyzing traffic patterns...")
analyzer.traffic_over_time('day')
analyzer.traffic_over_time('hour')
analyzer.traffic_over_time('day_of_week')

# Analyze traffic sources
print("\nAnalyzing traffic sources...")
analyzer.analyze_traffic_sources()

# Analyze popular pages
print("\nAnalyzing popular pages...")
analyzer.popular_pages()

print("\nAnalysis complete!")