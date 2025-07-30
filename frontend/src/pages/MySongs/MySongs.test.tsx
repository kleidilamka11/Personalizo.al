import MySongs from './MySongs';
import { render, screen, waitFor } from '../../testUtils';
import * as songService from '../../services/songService';
import * as orderService from '../../services/orderService';
import { BACKEND_BASE_URL } from '../../services/api';

jest.mock('../../services/songService');
jest.mock('../../services/orderService');

describe('MySongs page', () => {
  test('fetches and displays songs', async () => {
    (songService.getMySongs as jest.Mock).mockResolvedValue([
      {
        id: 1,
        order_id: 10,
        title: 'Song A',
        genre: 'pop',
        file_path: 'path',
        created_at: '',
      },
    ]);
    (orderService.getOrders as jest.Mock).mockResolvedValue([
      {
        id: 10,
        song_package_id: 1,
        recipient_name: 'x',
        mood: 'y',
        status: 'delivered',
        delivered_url: '/file.mp3',
      },
    ]);

    render(<MySongs />);

    await screen.findByText(/your songs/i);
    await waitFor(() =>
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument(),
    );

    expect(screen.getByText(/Title: Song A/i)).toBeInTheDocument();
    expect(screen.getByText(/Status: delivered/i)).toBeInTheDocument();
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
