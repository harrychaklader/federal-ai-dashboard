from flask import Flask, jsonify, request
from data_fetcher import DataFetcher
import os

app = Flask(__name__)

@app.route('/api/use-cases', methods=['GET'])
def get_use_cases():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('perPage', 10))
        search_query = request.args.get('searchQuery', '')
        agency = request.args.get('agency', '')
        topic = request.args.get('topic', '')
        status = request.args.get('status', '')

        fetcher = DataFetcher()
        data = fetcher.fetch_data()

        # Apply filters
        filtered_data = data
        if search_query:
            filtered_data = [item for item in filtered_data if search_query.lower() in str(item).lower()]
        if agency:
            filtered_data = [item for item in filtered_data if item['agency'] == agency]
        if topic:
            filtered_data = [item for item in filtered_data if item['topic'] == topic]
        if status:
            filtered_data = [item for item in filtered_data if item['status'] == status]

        # Calculate pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_data = filtered_data[start_idx:end_idx]

        return jsonify({
            'items': paginated_data,
            'total': len(filtered_data),
            'page': page,
            'perPage': per_page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    try:
        fetcher = DataFetcher()
        metadata = fetcher.get_metadata()
        return jsonify(metadata)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
