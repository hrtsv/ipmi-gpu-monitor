# IPMI GPU Monitor

This application monitors IPMI sensors and NVIDIA GPUs, provides dynamic fan control, and presents a secure, mobile-friendly web interface.

## Deployment

To deploy this application using Dockge, use the following command:

```
docker run -d \
  --name ipmi-gpu-monitor \
  --runtime=nvidia \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -p 5000:5000 \
  -v /opt/stacks/ipmi-gpu-monitor/data:/app/data \
  -e SECRET_KEY=your_secret_key_here \
  -e JWT_SECRET_KEY=your_jwt_secret_key_here \
  -e IPMI_HOST=your_ipmi_host \
  -e IPMI_USERNAME=your_ipmi_username \
  -e IPMI_PASSWORD=your_ipmi_password \
  --device /dev/ipmi0:/dev/ipmi0 \
  ghcr.io/yourusername/ipmi-gpu-monitor:latest
```

Replace the environment variable values with your actual configuration.

## First-time Login

After deployment, access the web interface at `http://your-server-ip:5000`.

Use the following default credentials to log in:
- Username: admin
- Password: changeme

**Important:** Change the default password immediately after your first login for security reasons.

## Features

- Real-time monitoring of IPMI sensors and NVIDIA GPUs
- Dynamic fan control based on temperature thresholds
- Secure, JWT-authenticated API
- Mobile-friendly web interface with real-time updates
- Historical data charts

For more information and advanced configuration options, please refer to the documentation.