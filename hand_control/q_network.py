import torch.nn as nn 



class Net(nn.Module):
    def __init__(self,num_state,num_action):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(num_state, 100)
        self.ReLu = nn.ReLU()
        self.fc2 = nn.Linear(100, num_action)

    def forward(self, x):
        x = self.fc1(x)
        x = self.ReLu(x)
        action_value = self.fc2(x)
        return action_value