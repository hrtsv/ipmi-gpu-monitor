docker run -d \
  --name ipmi-gpu-monitor \
  --runtime=nvidia \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -p 5000:5000 \
  -v /path/to/data:/app/data \
  -e SECRET_KEY=your_secret_key_here \
  -e JWT_SECRET_KEY=your_jwt_secret_key_here \
  -e IPMI_HOST=your_ipmi_host \
  -e IPMI_USERNAME=your_ipmi_username \
  -e IPMI_PASSWORD=your_ipmi_password \
  --device /dev/ipmi0:/dev/ipmi0 \
  ghcr.io/yourusername/ipmi-gpu-monitor:latest