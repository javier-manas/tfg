import torch

print("CUDA está disponible:", torch.cuda.is_available())
print("Versión de PyTorch:", torch.__version__)
print("Versión de CUDA:", torch.version.cuda)
