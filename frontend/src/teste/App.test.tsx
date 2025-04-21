import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';
import axios from 'axios';
import '@testing-library/jest-dom';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

test('can submit form to add bookmark', async () => {
  mockedAxios.get.mockResolvedValueOnce({ data: [] });
  mockedAxios.post.mockResolvedValue({ data: {} });
  mockedAxios.get.mockResolvedValueOnce({
    data: [
      {
        id: 1,
        title: 'Test Bookmark',
        url: 'http://test.com',
        remember_date: '2024-04-21'
      }
    ]
  });

  render(<App />);

  fireEvent.change(screen.getByPlaceholderText('Title'), {
    target: { value: 'Test Bookmark' },
  });
  fireEvent.change(screen.getByPlaceholderText('URL'), {
    target: { value: 'http://test.com' },
  });
  fireEvent.change(screen.getByPlaceholderText('Date'), {
    target: { value: '2024-04-21' },
  });

  fireEvent.click(screen.getByText('Add Bookmark'));

  await waitFor(() => {
    expect(screen.getByText('Test Bookmark')).toBeInTheDocument();
  });
});
