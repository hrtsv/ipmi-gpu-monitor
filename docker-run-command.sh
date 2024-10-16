docker run -d \
  --name ipmi-gpu-monitor \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e SECRET_KEY=your_secret_key_here \
  -e JWT_SECRET_KEY=your_jwt_secret_key_here \
  -e IPMI_HOST=your_ipmi_host \
  -e IPMI_USERNAME=your_ipmi_username \
  -e IPMI_PASSWORD=your_ipmi_password \
  -p 5000:5000 \
  -v /opt/stacks/ipmi-gpu-monitor/data:/app/data \
  --restart unless-stopped \
  ghcr.io/hrtsv/ipmi-gpu-monitor:main