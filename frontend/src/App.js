import { useState, useEffect } from 'react';
import {
  AppBar,
  Box,
  Button,
  Container,
  TextField,
  Toolbar,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import axios from 'axios';
import config from './config';

function App() {
  const [useCases, setUseCases] = useState([]);
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(25);
  const [totalItems, setTotalItems] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedAgency, setSelectedAgency] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [loading, setLoading] = useState(true);
  const [metadataLoading, setMetadataLoading] = useState(true);
  const [error, setError] = useState(null);
  const [metadata, setMetadata] = useState({
    agencies: [],
    topics: [],
    statuses: []
  });
  const [lastFilters, setLastFilters] = useState({
    search: '',
    agency: '',
    topic: '',
    status: ''
  });

  useEffect(() => {
    const fetchMetadata = async () => {
      setMetadataLoading(true);
      try {
        const metadataResponse = await axios.get(`${config.apiBaseUrl}/metadata`);
        setMetadata(metadataResponse.data);
        setError(null);
      } catch (err) {
        setError('Error loading filters. Please try again later.');
        console.error('Error fetching metadata:', err);
      } finally {
        setMetadataLoading(false);
      }
    };

    fetchMetadata();
    fetchUseCases(); // Initial data load
  }, []);

  const fetchUseCases = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (searchQuery) params.append('search', searchQuery);
      if (selectedAgency) params.append('agency', selectedAgency);
      if (selectedTopic) params.append('topic', selectedTopic);
      if (selectedStatus) params.append('status', selectedStatus);
      params.append('page', page);
      params.append('per_page', perPage);

      // Store current filters
      setLastFilters({
        search: searchQuery,
        agency: selectedAgency,
        topic: selectedTopic,
        status: selectedStatus
      });

      console.log('Fetching with params:', params.toString());
      const response = await axios.get(`${config.apiBaseUrl}/use-cases?${params.toString()}`);
      console.log('Received data:', response.data);
      
      setUseCases(response.data.items);
      setTotalItems(response.data.total_items);
      setTotalPages(response.data.total_pages);
      setError(null);
    } catch (err) {
      setError('Error fetching use cases. Please try again later.');
      console.error('Error fetching use cases:', err);
      console.error('Error details:', err.response?.data || err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUseCases();
  }, [searchQuery, selectedAgency, selectedTopic, selectedStatus, page, perPage]);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" sx={{ backgroundColor: '#1a237e' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Federal AI Use Case Inventory Dashboard
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4 }}>
        <Paper sx={{ p: 3, mb: 4 }}>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: metadataLoading ? 2 : 0 }}>
            {metadataLoading && (
              <Box sx={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
                <CircularProgress size={24} />
              </Box>
            )}
            <TextField
              label="Search Use Cases"
              variant="outlined"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              sx={{ flexGrow: 1, minWidth: '200px' }}
              placeholder="Search by name, purpose, or outputs"
            />
            <FormControl sx={{ minWidth: '250px' }} disabled={metadataLoading}>
              <InputLabel>Agency</InputLabel>
              <Select
                value={selectedAgency}
                label="Agency"
                onChange={(e) => {
                  const value = e.target.value;
                  console.log('Selected agency:', value);
                  setSelectedAgency(value);
                }}
              >
                <MenuItem value="">All Agencies</MenuItem>
                {metadata.agencies.map((agency) => (
                  <MenuItem key={agency} value={agency}>
                    {agency}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl sx={{ minWidth: '200px' }} disabled={metadataLoading}>
              <InputLabel>Topic</InputLabel>
              <Select
                value={selectedTopic}
                label="Topic"
                onChange={(e) => {
                  const value = e.target.value;
                  console.log('Selected topic:', value);
                  setSelectedTopic(value);
                }}
              >
                <MenuItem value="">All Topics</MenuItem>
                {metadata.topics.map((topic) => (
                  <MenuItem key={topic} value={topic}>{topic}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl sx={{ minWidth: '200px' }} disabled={metadataLoading}>
              <InputLabel>Status</InputLabel>
              <Select
                value={selectedStatus}
                label="Status"
                onChange={(e) => {
                  const value = e.target.value;
                  console.log('Selected status:', value);
                  setSelectedStatus(value);
                }}
              >
                <MenuItem value="">All Statuses</MenuItem>
                {metadata.statuses.map((status) => (
                  <MenuItem key={status} value={status}>{status}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl sx={{ minWidth: '150px' }} disabled={metadataLoading}>
              <InputLabel>Results per page</InputLabel>
              <Select
                value={perPage}
                label="Results per page"
                onChange={(e) => {
                  setPerPage(e.target.value);
                  setPage(1); // Reset to first page when changing results per page
                }}
              >
                <MenuItem value={25}>25</MenuItem>
                <MenuItem value={50}>50</MenuItem>
                <MenuItem value={100}>100</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </Paper>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }}>
              <TableHead>
                <TableRow sx={{ backgroundColor: '#e8eaf6' }}>
                  <TableCell><Typography variant="subtitle1" fontWeight="bold">Use Case Name</Typography></TableCell>
                  <TableCell><Typography variant="subtitle1" fontWeight="bold">Agency</Typography></TableCell>
                  <TableCell><Typography variant="subtitle1" fontWeight="bold">Topic</Typography></TableCell>
                  <TableCell><Typography variant="subtitle1" fontWeight="bold">Purpose</Typography></TableCell>
                  <TableCell><Typography variant="subtitle1" fontWeight="bold">Outputs</Typography></TableCell>
                  <TableCell><Typography variant="subtitle1" fontWeight="bold">Status</Typography></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {useCases.map((useCase) => (
                  <TableRow key={useCase.id}>
                    <TableCell>{useCase.name}</TableCell>
                    <TableCell>{`${useCase.agency} (${useCase.agency_abbrev})`}</TableCell>
                    <TableCell>{useCase.topic}</TableCell>
                    <TableCell sx={{ maxWidth: '300px', whiteSpace: 'normal', wordWrap: 'break-word' }}>
                      {useCase.purpose}
                    </TableCell>
                    <TableCell sx={{ maxWidth: '300px', whiteSpace: 'normal', wordWrap: 'break-word' }}>
                      {useCase.outputs}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={useCase.status}
                        color={
                          useCase.status.toLowerCase().includes('planning') ? 'default' :
                          useCase.status.toLowerCase().includes('development') ? 'info' :
                          useCase.status.toLowerCase().includes('testing') ? 'warning' :
                          useCase.status.toLowerCase().includes('production') ? 'success' :
                          'default'
                        }
                        size="small"
                        sx={{
                          textTransform: 'capitalize',
                          maxWidth: '200px',
                          whiteSpace: 'normal',
                          height: 'auto',
                          '& .MuiChip-label': {
                            whiteSpace: 'normal',
                            padding: '8px 4px'
                          }
                        }}
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}

        {!loading && !error && (
          <Box sx={{ mt: 4, mb: 4, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 2 }}>
            <Button
              variant="outlined"
              disabled={page === 1}
              onClick={() => setPage(p => p - 1)}
            >
              Previous
            </Button>
            <Typography>
              Page {page} of {totalPages} ({totalItems} total items)
            </Typography>
            <Button
              variant="outlined"
              disabled={page === totalPages}
              onClick={() => setPage(p => p + 1)}
            >
              Next
            </Button>
          </Box>
        )}
      </Container>
    </Box>
  );
}

export default App;
