## Deployment

To deploy the latest version of this application using Dockge, use the following command:

```bash
docker run -d \
  --name ipmi-gpu-monitor \
  --runtime=nvidia \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -p 5000:5000 \
  -v /opt/stacks/ipmi-gpu-monitor/data:/app/data \
  -e IPMI_HOST=your_ipmi_host \
  -e IPMI_USERNAME=your_ipmi_username \
  -e IPMI_PASSWORD=your_ipmi_password \
  --device /dev/ipmi0:/dev/ipmi0 \
  ghcr.io/hrtsv/ipmi-gpu-monitor:main

Replace the IPMI-related environment variable values with your actual configuration.

This command pulls the latest image from GitHub Container Registry, which is automatically updated whenever changes are pushed to the main branch of the repository. The SECRET_KEY and JWT_SECRET_KEY are automatically generated during the build process, ensuring unique keys for each deployment.
```