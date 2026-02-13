import matplotlib.pyplot as plt
import io
import random
import datetime

class SentimentVisualizer:
    """
    Generates visual representations of Aqulier Nexus intelligence data.
    """
    
    def generate_chart(self, ticker: str, data_points: list):
        """
        Creates a Price vs. Sentiment chart.
        """
        print(f"🎨 [Visualizer] Rendering chart for ${ticker}...")
        
        # Mock Data generation
        dates = [datetime.datetime.now() - datetime.timedelta(hours=i) for i in range(24)]
        prices = [random.randint(60000, 70000) for _ in range(24)]
        sentiment = [random.randint(20, 80) for _ in range(24)]
        
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Plot Price
        color = 'tab:green'
        ax1.set_xlabel('Time (Last 24h)')
        ax1.set_ylabel('Price (USDC)', color=color)
        ax1.plot(dates, prices, color=color, linewidth=2, label='Price')
        ax1.tick_params(axis='y', labelcolor=color)
        
        # Plot Sentiment
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Sentiment Score (0-100)', color=color)
        ax2.plot(dates, sentiment, color=color, linestyle='--', label='Sentiment')
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title(f"Aqulier Nexus: {ticker} Price vs. Sentiment Correlation")
        fig.tight_layout()
        
        # Save to buffer (in real app, this would be sent to frontend)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        print("✅ [Visualizer] Chart generated successfully.")
        return buf

    def generate_ascii_chart(self, score: int):
        """
        Generates a simple ASCII bar for terminal output.
        """
        bar_length = 20
        filled_length = int(bar_length * score // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        return f"Sentiment: [{bar}] {score}/100"

if __name__ == "__main__":
    viz = SentimentVisualizer()
    print(viz.generate_ascii_chart(75))
    viz.generate_chart("BTC", [])
