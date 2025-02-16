from github import Github
import os
import json
import tempfile
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv()

class DataFetcher:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo_name = 'ombegov/2024-Federal-AI-Use-Case-Inventory'
        self.file_path = 'data/2024_consolidated_ai_inventory_raw_v2.xls'
        self.cache = None
        self.last_fetch_time = None
        self.cache_duration = 3600  # Cache duration in seconds (1 hour)
        
        # Initialize Github client
        self.g = Github(self.github_token) if self.github_token else None
        if not self.g:
            print("No GitHub token found. Using sample data.")
        
        # Column mappings from Excel to our API
        self.column_mappings = {
            'Use Case Name': 'name',
            'Agency': 'agency',
            'Agency Abbreviation': 'agency_abbrev',
            'Use Case Topic Area': 'topic',
            'What is the intended purpose and expected benefits of the AI?': 'purpose',
            'Describe the AI system\'s outputs.': 'outputs',
            'Stage of Development': 'status'
        }

    def _should_refresh_cache(self):
        if not self.last_fetch_time:
            return True
        elapsed = (datetime.now() - self.last_fetch_time).total_seconds()
        return elapsed > self.cache_duration

    def fetch_data(self):
        """Fetch data from GitHub repository and cache it"""
        if self.cache and not self._should_refresh_cache():
            return self.cache

        if not self.g:
            print("No GitHub client available, using sample data")
            return self._get_sample_data()

        try:
            print(f"Fetching data from GitHub repository: {self.repo_name}")
            # Get the repository and file content
            repo = self.g.get_repo(self.repo_name)
            file_content = repo.get_contents(self.file_path)
            download_url = file_content.download_url

            print(f"Downloading Excel file from: {download_url}")
            # Download the Excel file to a temporary file
            response = requests.get(download_url)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            with tempfile.NamedTemporaryFile(suffix='.xls', delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
                print(f"Saved Excel file to temporary location: {temp_file_path}")

            print("Reading Excel file with pandas")
            # Read the Excel file
            df = pd.read_excel(temp_file_path, engine='xlrd')

            # Clean up the temporary file
            os.unlink(temp_file_path)
            print("Successfully read Excel file and cleaned up temporary file")

            # Process the data
            processed_data = []
            for _, row in df.iterrows():
                # Extract and clean each field
                name = row.get('Use Case Name')
                agency = row.get('Agency')
                agency_abbrev = row.get('Agency Abbreviation')
                topic = row.get('Use Case Topic Area')
                purpose = row.get('What is the intended purpose and expected benefits of the AI?')
                outputs = row.get('Describe the AI system\'s outputs.')
                status = row.get('Stage of Development')
                
                # Skip row if essential fields are missing
                if pd.isna(name) or pd.isna(agency):
                    continue
                    
                processed_item = {
                    'id': str(len(processed_data) + 1),
                    'name': str(name if not pd.isna(name) else ''),
                    'agency': str(agency if not pd.isna(agency) else ''),
                    'agency_abbrev': str(agency_abbrev if not pd.isna(agency_abbrev) else ''),
                    'topic': str(topic if not pd.isna(topic) else ''),
                    'purpose': str(purpose if not pd.isna(purpose) else ''),
                    'outputs': str(outputs if not pd.isna(outputs) else ''),
                    'status': str(status if not pd.isna(status) else '').strip()
                }
                # Only add items with non-empty and non-nan status
                if processed_item['status'] and processed_item['status'].lower() != 'nan':
                    processed_data.append(processed_item)

            self.cache = processed_data
            self.last_fetch_time = datetime.now()
            return processed_data

        except Exception as e:
            error_msg = f"Error fetching data from GitHub: {str(e)}"
            print(error_msg)
            if hasattr(e, '__traceback__'):
                import traceback
                print("Full traceback:")
                print(''.join(traceback.format_tb(e.__traceback__)))
            
            # Check if it's an authentication error
            if 'Bad credentials' in str(e):
                print("GitHub authentication failed. Please check your token.")
            elif '404' in str(e):
                print("Repository or file not found. Please check the repository and file path.")
            elif '403' in str(e):
                print("Rate limit exceeded or insufficient permissions.")
                
            return self._get_sample_data()

    def _get_sample_data(self):
        """Return sample data when data fetch fails"""
        return [
            {
                'id': '1',
                'name': 'Document Processing Automation',
                'agency': 'Department of Veterans Affairs',
                'agency_abbrev': 'VA',
                'topic': 'Document Processing',
                'purpose': 'To automate the processing of veteran benefit claims using AI and machine learning.',
                'outputs': 'Processed claim documents with extracted key information.',
                'status': 'In Development'
            },
            {
                'id': '2',
                'name': 'Predictive Maintenance System',
                'agency': 'Department of Defense',
                'agency_abbrev': 'DOD',
                'topic': 'Maintenance',
                'purpose': 'To predict equipment failures and optimize maintenance schedules.',
                'outputs': 'Maintenance predictions and risk assessments.',
                'status': 'In Production'
            },
            {
                'id': '3',
                'name': 'Climate Change Impact Analysis',
                'agency': 'Environmental Protection Agency',
                'agency_abbrev': 'EPA',
                'topic': 'Environmental Analysis',
                'purpose': 'To analyze and predict climate change impacts using AI models.',
                'outputs': 'Climate impact predictions and recommendations.',
                'status': 'In Testing'
            },
            {
                'id': '4',
                'name': 'Cybersecurity Threat Detection',
                'agency': 'Department of Homeland Security',
                'agency_abbrev': 'DHS',
                'topic': 'Cybersecurity',
                'purpose': 'To detect and prevent cybersecurity threats using AI.',
                'outputs': 'Threat detection alerts and assessments.',
                'status': 'Planning'
            },
            {
                'id': '5',
                'name': 'Healthcare Analytics Platform',
                'agency': 'Department of Health and Human Services',
                'agency_abbrev': 'HHS',
                'topic': 'Healthcare',
                'purpose': 'To analyze healthcare data for improved patient outcomes.',
                'outputs': 'Healthcare analytics and patient risk scores.',
                'status': 'In Development'
            },
            {
                'id': '6',
                'name': 'Tax Fraud Detection System',
                'agency': 'Department of the Treasury',
                'agency_abbrev': 'TREAS',
                'topic': 'Fraud Detection',
                'purpose': 'To identify potential tax fraud using machine learning.',
                'outputs': 'Fraud risk scores and investigation recommendations.',
                'status': 'In Production'
            }
        ]

    def search_use_cases(self, query=None, agency=None, topic=None, status=None):
        """Search and filter use cases based on criteria"""
        try:
            print(f"Searching use cases with filters - Query: {query}, Agency: {agency}, Topic: {topic}, Status: {status}")
            data = self.fetch_data()
            filtered_data = data

            if query:
                query = query.lower()
                filtered_data = [
                    case for case in filtered_data
                    if query in case['name'].lower() or
                       query in case['purpose'].lower() or
                       query in case['outputs'].lower()
                ]
                print(f"After query filter: {len(filtered_data)} results")

            if agency:
                # Extract agency name from combined format "Agency Name (ABBREV)"
                agency = agency.lower()
                if '(' in agency:
                    agency_name = agency.split('(')[0].strip().lower()
                    agency_abbrev = agency.split('(')[1].replace(')', '').strip().lower()
                    filtered_data = [
                        case for case in filtered_data
                        if case['agency'].lower() == agency_name or
                           case['agency_abbrev'].lower() == agency_abbrev
                    ]
                else:
                    filtered_data = [
                        case for case in filtered_data
                        if case['agency'].lower() == agency or
                           case['agency_abbrev'].lower() == agency
                    ]
                print(f"After agency filter: {len(filtered_data)} results")

            if topic:
                topic = topic.lower()
                filtered_data = [
                    case for case in filtered_data
                    if case['topic'].lower() == topic
                ]
                print(f"After topic filter: {len(filtered_data)} results")

            if status:
                status = status.lower()
                filtered_data = [
                    case for case in filtered_data
                    if case['status'] and 
                    case['status'].lower() != 'nan' and 
                    case['status'].lower() == status
                ]
                print(f"After status filter: {len(filtered_data)} results")

            print(f"Final result count: {len(filtered_data)}")
            return filtered_data

        except Exception as e:
            error_msg = f"Error in search_use_cases: {str(e)}"
            print(error_msg)
            if hasattr(e, '__traceback__'):
                import traceback
                print("Full traceback:")
                print(''.join(traceback.format_tb(e.__traceback__)))
            return []

        return filtered_data

    def get_metadata(self):
        """Get unique values for filtering"""
        try:
            print("Fetching metadata for filters...")
            data = self.fetch_data()
            
            agencies = sorted(set(
                f"{case['agency']} ({case['agency_abbrev']})" 
                for case in data 
                if case['agency'] and case['agency_abbrev']
            ))
            topics = sorted(set(case['topic'] for case in data if case['topic']))
            statuses = sorted(set(
                case['status'] for case in data 
                if case['status'] and case['status'].lower() != 'nan'
            ))
            
            metadata = {
                'agencies': agencies,
                'topics': topics,
                'statuses': statuses
            }
            
            print(f"Metadata summary:")
            print(f"- Number of agencies: {len(agencies)}")
            print(f"- Number of topics: {len(topics)}")
            print(f"- Number of statuses: {len(statuses)}")
            
            return metadata

        except Exception as e:
            error_msg = f"Error in get_metadata: {str(e)}"
            print(error_msg)
            if hasattr(e, '__traceback__'):
                import traceback
                print("Full traceback:")
                print(''.join(traceback.format_tb(e.__traceback__)))
            return {
                'agencies': [],
                'topics': [],
                'statuses': []
            }
