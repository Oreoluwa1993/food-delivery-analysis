# Food Delivery Analysis MVP

This project analyzes food delivery platforms (Foodora and Wolt) in Norway, comparing vendor data, cuisines, and pricing across different cities.

## Features

- Scrapes vendor data from Foodora.no and Wolt.no
- Analyzes vendor distribution across cities
- Compares cuisine types and pricing
- Generates JSON reports with timestamps
- Supports scheduled runs

## Setup

### Prerequisites

- Docker
- Docker Compose

### Local Deployment

1. Clone the repository:
```bash
git clone https://github.com/Oreoluwa1993/food-delivery-analysis.git
cd food-delivery-analysis
```

2. Create data directory:
```bash
mkdir data
```

3. Build and run with Docker Compose:
```bash
docker-compose up -d
```

### Cloud Deployment (AWS EC2)

1. Launch an EC2 instance
2. Install Docker and Docker Compose:
```bash
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. Clone and run:
```bash
git clone https://github.com/Oreoluwa1993/food-delivery-analysis.git
cd food-delivery-analysis
mkdir data
docker-compose up -d
```

## Configuration

- Set the `SCHEDULE_INTERVAL` environment variable in docker-compose.yml to control how often the analysis runs (in hours)
- Add or remove cities in food_delivery_mvp.py

## Output

Analysis results are saved in the `data` directory with timestamps:
```
data/food_delivery_analysis_YYYYMMDD_HHMMSS.json
```

## Monitoring

Check container logs:
```bash
docker-compose logs -f
```

## License

MIT