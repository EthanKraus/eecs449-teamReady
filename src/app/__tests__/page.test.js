import axios from 'axios';
import { render, fireEvent, waitFor } from '@testing-library/react';
import Home from '../page';

describe('End-to-end search flow', () => {
  test('User search query gets processed correctly', async () => {
    const { getByPlaceholderText, getByText } = render(<Home />);
    
    // Simulate user typing a query
    const input = getByPlaceholderText('Type your message...');
    fireEvent.change(input, { 
      target: { value: 'I want to buy a red dress under $100' } 
    });
    
    // Simulate form submission
    const submitButton = getByText('Send');
    fireEvent.click(submitButton);
    
    // Wait for and verify results
    await waitFor(() => {
      // Check if products are displayed
      expect(document.body.textContent).toContain('Found');
      expect(document.body.textContent).toContain('products');
    });
  });
}); 