import { render, screen } from '@testing-library/react';
import App from './App';

// Mock axios to avoid parsing its ESM build during tests
jest.mock('axios', () => ({
  __esModule: true,
  default: { get: jest.fn() },
  get: jest.fn()
}));

test('renders Use Case Name heading', async () => {
  const axios = require('axios');

  // Mock the metadata and use case responses
  axios.default.get
    .mockResolvedValueOnce({
      data: { agencies: [], topics: [], statuses: [] }
    })
    .mockResolvedValueOnce({
      data: {
        items: [
          {
            id: 1,
            name: 'Test Case',
            agency: 'Agency',
            agency_abbrev: 'A',
            topic: 'Topic',
            purpose: 'Purpose',
            outputs: 'Outputs',
            status: 'Testing'
          }
        ],
        total_items: 1,
        total_pages: 1
      }
    });

  render(<App />);

  const headingElement = await screen.findByText(/Use Case Name/i);
  expect(headingElement).toBeInTheDocument();
});
