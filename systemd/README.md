# Systemd Service Files

These systemd service files allow Infinite Server26 to run as a system service and start automatically on boot.

## Installation

### 1. Copy service file

```bash
sudo cp systemd/infinite-fortress.service /etc/systemd/system/
```

### 2. Set correct permissions

```bash
sudo chmod 644 /etc/systemd/system/infinite-fortress.service
```

### 3. Reload systemd

```bash
sudo systemctl daemon-reload
```

### 4. Enable service

```bash
sudo systemctl enable infinite-fortress
```

### 5. Start service

```bash
sudo systemctl start infinite-fortress
```

## Usage

### Start service
```bash
sudo systemctl start infinite-fortress
```

### Stop service
```bash
sudo systemctl stop infinite-fortress
```

### Restart service
```bash
sudo systemctl restart infinite-fortress
```

### Check status
```bash
sudo systemctl status infinite-fortress
```

### View logs
```bash
sudo journalctl -u infinite-fortress -f
```

### Enable auto-start on boot
```bash
sudo systemctl enable infinite-fortress
```

### Disable auto-start
```bash
sudo systemctl disable infinite-fortress
```

## Requirements

- Docker must be installed and running
- Docker Compose must be installed
- Repository must be cloned to `/opt/infinite-server26`
- `.env` file must exist in `/opt/infinite-server26`

## Troubleshooting

### Service fails to start

Check logs:
```bash
sudo journalctl -u infinite-fortress -n 50
```

Check Docker:
```bash
sudo systemctl status docker
```

### Permission issues

Ensure Docker socket is accessible:
```bash
sudo usermod -aG docker $USER
```

### Path issues

Verify WorkingDirectory in service file matches your installation path.

Default is `/opt/infinite-server26`, change if needed:
```bash
sudo nano /etc/systemd/system/infinite-fortress.service
# Edit WorkingDirectory line
sudo systemctl daemon-reload
sudo systemctl restart infinite-fortress
```

## Notes

- The service uses `Type=oneshot` with `RemainAfterExit=yes` to properly track docker-compose managed containers
- Automatic restart on failure is enabled with 30 second delay
- Service will pull latest images before starting (can be disabled by removing ExecStartPre)
- Logs are sent to systemd journal (view with journalctl)
