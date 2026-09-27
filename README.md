# Simple Docker Compose DevOps Lab

A deliberately small lab containing:

- Nginx web server
- MySQL database
- Elasticsearch
- Docker Compose networking
- Persistent Docker volumes

There is intentionally almost no application/programming code.

## 1. Start

```bash
cd simple-docker-compose-lab
docker compose up -d
```

## 2. Check containers

```bash
docker compose ps
```

Expected services:

- simple-web
- simple-mysql
- simple-elasticsearch

## 3. Open the web page

From your browser:

```text
http://SERVER-IP:8080
```

If this is an EC2 instance, allow TCP 8080 in the EC2 Security Group.

## 4. Check logs

```bash
docker compose logs web
docker compose logs mysql
docker compose logs elasticsearch
```

Follow logs:

```bash
docker compose logs -f
```

## 5. Test Docker networking

Enter the web container:

```bash
docker exec -it simple-web sh
```

Inside the container:

```bash
ping mysql
```

If ping is not installed, use:

```bash
wget -qO- http://elasticsearch:9200
```

Exit:

```bash
exit
```

The important concept is that Docker Compose creates a network and services can reach each other by service name:

```text
mysql
elasticsearch
web
```

## 6. Test MySQL

```bash
docker exec -it simple-mysql mysql -udevops -pdevopspass devopsdb
```

Inside MySQL:

```sql
SHOW DATABASES;
SHOW TABLES;
exit
```

## 7. Test Elasticsearch

From the Docker host:

```bash
docker exec simple-elasticsearch curl http://localhost:9200
```

You should receive JSON containing Elasticsearch information.

## 8. Check volumes

```bash
docker volume ls
```

You should see volumes similar to:

```text
simple-docker-compose-lab_mysql_data
simple-docker-compose-lab_elastic_data
```

## 9. Stop

```bash
docker compose down
```

This removes the containers but keeps the named volumes.

## 10. Stop and DELETE all data

WARNING: this removes MySQL and Elasticsearch data.

```bash
docker compose down -v
```

## 11. Rebuild from scratch

```bash
docker compose down -v
docker compose up -d
docker compose ps
```

## Architecture

```text
                    Docker Compose Network
                           |
              +------------+------------+
              |            |            |
          +---v---+    +---v----+   +--v-------------+
          | Nginx |    | MySQL  |   | Elasticsearch   |
          | :80   |    | :3306  |   | :9200          |
          +---+---+    +--------+   +----------------+
              |
         Host :8080
              |
        Browser / User
```

## What you should learn from this lab

This project is intentionally NOT a programming project.

Focus on:

1. `docker compose up/down`
2. Container names
3. Service names
4. Docker Compose network
5. Port mapping
6. Environment variables
7. Named volumes
8. `depends_on`
9. Container logs
10. `docker exec`
11. Troubleshooting container status
12. Checking connectivity between containers

After this works, the next useful DevOps exercise is to add a small backend API between Nginx and MySQL/Elasticsearch. That can be a separate advanced lab.
