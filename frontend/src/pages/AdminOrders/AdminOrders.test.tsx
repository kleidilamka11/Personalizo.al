import AdminOrders from './AdminOrders'
import { render, screen, waitFor } from '../../testUtils'
import * as adminService from '../../services/adminService'

jest.mock('../../services/adminService')

describe('AdminOrders page', () => {
  test('fetches and displays admin orders', async () => {
    ;(adminService.getAllOrders as jest.Mock).mockResolvedValue([
      {
        id: 1,
        recipient_name: 'Rec',
        mood: 'happy',
        facts: null,
        status: 'pending',
        delivered_url: null,
        created_at: '2024-01-01',
        user: { id: 1, email: 'admin@test.com' },
        package: { id: 2, name: 'Gold' },
      },
    ])

    render(<AdminOrders />)

    await screen.findByText(/all orders/i)
    await waitFor(() =>
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument(),
    )

    expect(screen.getByText(/admin@test.com/i)).toBeInTheDocument()
    expect(screen.getByText(/Status: pending/i)).toBeInTheDocument()
  })
})
