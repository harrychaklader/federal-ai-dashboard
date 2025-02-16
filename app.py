from flask import Flask, jsonify, request
from flask_cors import CORS
from data_fetcher import DataFetcher
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the data fetcher
data_fetcher = DataFetcher()



@app.route('/api/use-cases', methods=['GET'])
def get_use_cases():
    # Get query parameters
    search_query = request.args.get('search', '')
    agency_filter = request.args.get('agency', '')
    topic_filter = request.args.get('topic', '')
    status_filter = request.args.get('status', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 25))
    
    try:
        # Use the data fetcher to search and filter use cases
        filtered_cases = data_fetcher.search_use_cases(
            query=search_query,
            agency=agency_filter,
            topic=topic_filter,
            status=status_filter
        )
        
        # Calculate pagination
        total_items = len(filtered_cases)
        total_pages = (total_items + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_data = filtered_cases[start_idx:end_idx]
        
        return jsonify({
            'items': paginated_data,
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page,
            'per_page': per_page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    try:
        # Get metadata for filters
        metadata = data_fetcher.get_metadata()
        return jsonify(metadata)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
