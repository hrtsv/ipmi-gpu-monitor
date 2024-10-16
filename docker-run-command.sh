version: '3'
services:
  ipmi-gpu-monitor:
    image: ghcr.io/hrtsv/ipmi-gpu-monitor:main
    container_name: ipmi-gpu-monitor
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - SECRET_KEY=your_secret_key_here
      - JWT_SECRET_KEY=your_jwt_secret_key_here
      - IPMI_HOST=your_ipmi_host
      - IPMI_USERNAME=your_ipmi_username
      - IPMI_PASSWORD=your_ipmi_password
    ports:
      - "5000:5000"
    volumes:
      - /opt/stacks/ipmi-gpu-monitor/data:/app/data
    devices:
      - /dev/nvidia0:/dev/nvidia0
      - /dev/nvidiactl:/dev/nvidiactl
      - /dev/nvidia-modeset:/dev/nvidia-modeset
      - /dev/nvidia-uvm:/dev/nvidia-uvm
    restart: unless-stopped