docker run -d \
  --name ipmi-gpu-monitor \
  --gpus all \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -p 5000:5000 \
  -v /opt/stacks/ipmi-gpu-monitor/data:/app/data \
  -e SECRET_KEY=your_secret_key_here \
  -e IPMI_HOST=your_ipmi_host \
  -e IPMI_USERNAME=your_ipmi_username \
  -e IPMI_PASSWORD=your_ipmi_password \
  ghcr.io/hrtsv/ipmi-gpu-monitor:main
