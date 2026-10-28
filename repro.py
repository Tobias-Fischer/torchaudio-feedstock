import platform
import traceback

import torch
import torch.nn.functional as F

print("torch", torch.__version__, platform.machine())
print("quantized engines:", torch.backends.quantized.supported_engines, "current:", torch.backends.quantized.engine)
print(torch.__config__.show())

# torchaudio lfilter -> DifferentiableFIR: depthwise conv1d with kernel size 4
for groups in (1, 2, 3):
    x = torch.rand(1, groups, 44103)
    w = torch.rand(groups, 1, 4)
    try:
        F.conv1d(x, w, groups=groups)
        print(f"conv1d groups={groups}: OK")
    except Exception:
        print(f"conv1d groups={groups}: FAILED")
        traceback.print_exc()

# torchaudio wav2vec2 test_quantize -> dynamic quantization of nn.Linear
try:
    model = torch.nn.Sequential(torch.nn.Linear(8, 8))
    torch.ao.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
    print("quantize_dynamic: OK")
except Exception:
    print("quantize_dynamic: FAILED")
    traceback.print_exc()
