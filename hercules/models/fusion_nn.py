import torch
import torch.nn as nn

class FusionNN(nn.Module):
    def __init__(self, binary_task=False):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(2, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid() if binary_task else nn.Identity()
        )

    def forward(self, x):
        return self.fc(x)

