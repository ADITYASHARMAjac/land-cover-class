import torch.nn as nn
import torchvision.models as models
import torch
import config


class LULC_Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = models.wide_resnet50_2(pretrained=True)
        n_inputs = self.network.fc.in_features
        self.network.fc = nn.Sequential(
                              nn.Linear(n_inputs, 256),
                              nn.ReLU(),
                              nn.Dropout(0.5),
                              nn.Linear(256, config.NUM_CLASSES),
                              nn.LogSoftmax(dim=1)
                                )
    def forward(self, xb):
        return self.network(xb)
    
    def freeze(self):
        for param in self.network.parameters():
            param.requires_grad = False
        for param in self.network.fc.parameters():
            param.requires_grad = True
    def unfreeze(self):
        for param in self.network.parameters():
            param.requires_grad = True
            
def get_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = LULC_Model()
    state_dict = torch.load(config.MODEL_PATH, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model