import Orders from './Orders';
import { render, screen, waitFor } from '../../testUtils';
import * as orderService from '../../services/orderService';
import * as packageService from '../../services/songPackageService';

jest.mock('../../services/orderService');
jest.mock('../../services/songPackageService');

describe('Orders page', () => {
  test('fetches and displays orders', async () => {
    (orderService.getOrders as jest.Mock).mockResolvedValue([
      {
        id: 1,
        song_package_id: 2,
        recipient_name: 'John',
        mood: 'happy',
        status: 'pending',
      },
    ]);
    (packageService.getSongPackages as jest.Mock).mockResolvedValue([
      { id: 2, name: 'Gold', price_eur: 10, description: 'desc' },
    ]);

    render(<Orders />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
    await waitFor(() => screen.getByText(/your orders/i));

    expect(screen.getByText(/package: Gold/i)).toBeInTheDocument();
    expect(screen.getByText(/Status: pending/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument();
  });
});
