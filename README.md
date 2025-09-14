# Persistent DB Docker Flask Application

## Overview

This is a simple Flask server application demonstrating Docker containerization with persistent database storage. The application uses Python, SQLite, and SQLAlchemy to create a single-page user registration and validation system.

**Key Learning Objective:** Understanding how to maintain database persistence across multiple Docker containers, even when containers are stopped or deleted.

### Recommended Activity
1. Build and run a container
2. Add users to the database
3. Create a second container and verify data persistence
4. Stop/delete both containers
5. Start a new container and confirm data still exists

---

## Prerequisites

- Docker installed on your system
- Basic understanding of command line operations
- Python 3.x (for local development)

---

## Docker Commands Reference

### Building Images

**Build image from current directory:**
```bash
docker build -t flask-docker-demo .
```

**Build from specific Dockerfile:**
```bash
docker build -t img -f other.Dockerfile .
```

### Running Containers

**Basic detached run:**
```bash
docker run -d flask-docker-demo
```

**Enhanced run with naming and port mapping:**
```bash
docker run -d --name flask-1 -p 5000:5000 flask-docker-demo
```

**Full command with volume mounting (recommended):**
```bash
docker run -d --name flask-1 -p 5000:5000 -v $(pwd)/instance:/app/instance -v $(pwd)/logs:/app/logs flask-docker-demo
```

**Running a second container for persistence testing:**
```bash
docker run -d --name flask-2 -p 5001:5000 -v $(pwd)/instance:/app/instance flask-docker-demo
```

### Container Management

**List running containers:**
```bash
docker ps
```

**List all containers (including stopped):**
```bash
docker ps -a
```

**Stop a container:**
```bash
docker stop
```

**Remove a stopped container:**
```bash
docker rm
```

**Remove all stopped containers:**
```bash
docker container prune
```

**Remove everything (use with caution):**
```bash
docker system prune -a
```

---

## Advanced Docker Features

### Volume Mounting Options

**Database persistence:**
```bash
-v $(pwd)/instance:/app/instance
```

**Log file persistence:**
```bash
-v $(pwd)/logs:/app/logs
```

**Custom container name:**
```bash
--name flask-demo
```

### Resource Limiting

**Limit CPU usage to 50%:**
```bash
--cpus="0.5"
```

**Limit memory to 256MB:**
```bash
--memory="256m"
```

### Container Access

**Access bash console in running container:**
```bash
docker exec -it  /bin/bash
```

---

## Docker Hub Integration

### Authentication and Publishing

**Login to Docker Hub:**
```bash
docker login -u
```

**Tag image for upload:**
```bash
docker tag  /:
```

**Push to Docker Hub:**
```bash
docker push /:
```

---

## Python Environment Management

### Virtual Environment Setup

Creating isolated Python environments is crucial for clean dependency management:

**Create virtual environment:**
```bash
python3 -m venv venv
```

**Activate environment:**
```bash
source venv/bin/activate
```

**Deactivate when finished:**
```bash
deactivate
```

**Generate requirements file:**
```bash
pip freeze > requirements.txt
```

### Benefits of Virtual Environments

- Isolates project dependencies
- Prevents conflicts between different projects
- Makes Docker builds more predictable
- Easier to manage Python packages

**Testing Isolation:**
Run `pip freeze` before and after activating your virtual environment to see the difference in available packages.

---

## Useful Bulk Operations

**Remove all containers of specific type:**
```bash
docker ps -aq | xargs docker rm
```

**Stop all running containers:**
```bash
docker ps -q | xargs docker stop
```

---

## Database Persistence Verification

### Step-by-Step Testing Process

1. **Start first container:**
   ```bash
   docker run -d --name flask-test-1 -p 5000:5000 -v $(pwd)/instance:/app/instance flask-docker-demo
   ```

2. **Add users via web interface at `localhost:5000`**

3. **Start second container:**
   ```bash
   docker run -d --name flask-test-2 -p 5001:5000 -v $(pwd)/instance:/app/instance flask-docker-demo
   ```

4. **Verify data exists at `localhost:5001`**

5. **Clean up:**
   ```bash
   docker stop flask-test-1 flask-test-2
   docker rm flask-test-1 flask-test-2
   ```

6. **Start new container and verify persistence:**
   ```bash
   docker run -d --name flask-test-3 -p 5000:5000 -v $(pwd)/instance:/app/instance flask-docker-demo
   ```

---

## Troubleshooting

### Common Issues

- **Port already in use:** Change the host port (e.g., `-p 5001:5000`)
- **Permission denied:** Ensure Docker daemon is running and user has proper permissions
- **Database not persisting:** Verify volume mount paths are correct
- **Container won't start:** Check `docker logs <container_name>` for error messages

### Debugging Commands

**View container logs:**
```bash
docker logs
```

**Inspect container details:**
```bash
docker inspect
```

**Check resource usage:**
```bash
docker stats
```

---

## Next Steps

This application serves as a foundation for more complex Docker deployments. Consider exploring:

- Multi-container applications with Docker Compose
- Container orchestration with Kubernetes
- CI/CD pipelines with Docker
- Production deployment strategies
- Security best practices for containerized applications

---

*This guide demonstrates fundamental Docker concepts through practical database persistence examples. The simple Flask application provides a hands-on learning environment for understanding container lifecycle management and data persistence strategies.*