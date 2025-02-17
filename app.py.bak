from flask import Flask, jsonify, request
from flask_cors import CORS
from data_fetcher import DataFetcher
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://federal-ai-dashboard.vercel.app"
        ]
    }
})

# Initialize the data fetcher
data_fetcher = DataFetcher()



@app.route('/api/use-cases', methods=['GET'])
def get_use_cases():
    print('Received request for use-cases')
    # Get query parameters
    search_query = request.args.get('search', '')
    agency_filter = request.args.get('agency', '')
    topic_filter = request.args.get('topic', '')
    status_filter = request.args.get('status', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 25))
    
    print(f'Query parameters: search={search_query}, agency={agency_filter}, topic={topic_filter}, status={status_filter}, page={page}, per_page={per_page}')
    
    try:
        print('Fetching data from GitHub...')
        # Use the data fetcher to search and filter use cases
        filtered_cases = data_fetcher.search_use_cases(
            query=search_query,
            agency=agency_filter,
            topic=topic_filter,
            status=status_filter
        )
        print(f'Found {len(filtered_cases)} matching cases')
        
        # Calculate pagination
        total_items = len(filtered_cases)
        total_pages = (total_items + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_data = filtered_cases[start_idx:end_idx]
        
        response_data = {
            'items': paginated_data,
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page,
            'per_page': per_page
        }
        print('Sending response:', response_data)
        return jsonify(response_data)
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
    # Use environment variables for port, defaulting to 5001 for local development
    port = int(os.environ.get('PORT', 5001))
    # In production, host should be '0.0.0.0' to accept all incoming connections
    host = '0.0.0.0' if os.environ.get('RENDER') else 'localhost'
    app.run(host=host, port=port, debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true')
