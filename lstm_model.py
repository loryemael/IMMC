import torch
import torch.nn as nn
import torch.optim as optim


class SimpleLSTM(nn.Module):
    """A simple LSTM model for sequence prediction."""

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        output_size: int,
        num_layers: int = 1,
        bidirectional: bool = False,
    ):
        super(SimpleLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.bidirectional = bidirectional

        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=bidirectional,
        )
        direction_factor = 2 if bidirectional else 1
        self.fc = nn.Linear(hidden_size * direction_factor, output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the LSTM network.

        Args:
            x: Input tensor of shape (batch_size, seq_len, input_size).
        Returns:
            Output tensor of shape (batch_size, output_size).
        """
        # Match the hidden state to the input device and dtype.
        h0 = x.new_zeros(
            self.num_layers * (2 if self.bidirectional else 1),
            x.size(0),
            self.hidden_size,
        )
        c0 = x.new_zeros(
            self.num_layers * (2 if self.bidirectional else 1),
            x.size(0),
            self.hidden_size,
        )

        out, _ = self.lstm(x, (h0, c0))
        # Use the last time step as the sequence representation.
        out = out[:, -1, :]
        out = self.fc(out)
        return out


if __name__ == "__main__":
    # Synthetic regression task:
    # use a sequence of 10 timesteps with 5 features to predict 1 value.
    torch.manual_seed(42)
    batch_size = 16
    seq_len = 10
    input_size = 5
    hidden_size = 32
    output_size = 1
    num_layers = 2
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Build a simple target from the input so training has a learnable pattern.
    X = torch.randn(batch_size, seq_len, input_size, device=device)
    y = X[:, :, 0].sum(dim=1, keepdim=True) * 0.3 + X[:, -1, 1:2] * 0.7

    model = SimpleLSTM(input_size, hidden_size, output_size, num_layers).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    # Training loop.
    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        preds = model(X)
        loss = criterion(preds, y)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1}, loss={loss.item():.4f}")

    model.eval()
    with torch.no_grad():
        sample_pred = model(X[:3])

    print("Predictions:")
    print(sample_pred.squeeze(-1).cpu())
    print("Targets:")
    print(y[:3].squeeze(-1).cpu())
