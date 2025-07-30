import Orders from './Orders';
import { render, screen, waitFor } from '../../testUtils';
import * as orderService from '../../services/orderService';
import * as packageService from '../../services/songPackageService';
import { BACKEND_BASE_URL } from '../../services/api';

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
      {
        id: 2,
        song_package_id: 2,
        recipient_name: 'Jane',
        mood: 'sad',
        status: 'delivered',
        delivered_url: '/file.mp3',
      },
    ]);
    (packageService.getSongPackages as jest.Mock).mockResolvedValue([
      { id: 2, name: 'Gold', price_eur: 10, description: 'desc' },
    ]);

    render(<Orders />);

    await screen.findByText(/your orders/i);
    await waitFor(() =>
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument(),
    );

    expect(screen.getAllByText(/package: Gold/i)).toHaveLength(2);
    expect(screen.getByText(/Status: pending/i)).toBeInTheDocument();
    expect(screen.getByText(/Status: delivered/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument();
    expect(screen.getByTestId('audio-player')).toHaveAttribute(
      'src',
      `${BACKEND_BASE_URL}/file.mp3`,
    );
    expect(screen.getByTestId('download-link')).toHaveAttribute(
      'href',
      `${BACKEND_BASE_URL}/file.mp3`,
    );
    expect(screen.getByTestId('download-link')).toHaveAttribute('download');
  });
});
