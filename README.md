# Web Scraping and BigQuery Ingest Project

This project performs web scraping from a webpage, processes the data, and loads it into Google BigQuery. The project is containerized with Docker to facilitate execution in different environments.

## Requirements

- Docker
- Docker Compose
- Google Cloud SDK (optional, for local testing)

## Project Structure

challenge_borda 
- docker-compose.yml 
- Dockerfile 
-   scraping.py 
  - requirements.txt 
  - challenge-borda-80fb1feb52cb.json 
-  deploy.sh

## Setup

### 1. Clone the Repository

Clone the repository from GitHub:

```bash
git clone https://github.com/your_username/challenge_Scraping-and-Ingest.git
cd challenge_Scraping-and-Ingest
```
### 2. Create a Docker Secret
#### Ensure that the file challenge-borda-80fb1feb52cb.json is in the same folder as your docker-compose.yml, and create a Docker secret:

```bash
docker secret create google_credentials challenge-borda-80fb1feb52cb.json

```

### 3. Build and Run the Container
#### Use Docker Compose to build and run the services:

```bash
docker-compose up --build
```

### 4. docker-compose logs
#### To check that the container is running correctly and to review logs, use:
```bash
docker-compose logs
```

### 5. Deploy the Container (Optional)
#### If you want to deploy the container to a production environment or Google Cloud Run, use the deploy.sh script. Make sure the script has execution permissions:

```bash
chmod +x deploy.sh
./deploy.sh
```


## How It Works
#### Scraping: The scraping.py script uses Selenium to perform web scraping on the Yogonet page, extracting the title, kicker, image, and other relevant data.

#### Data Processing: The extracted data is processed and temporarily saved in a CSV file.

#### BigQuery Load: The CSV file is loaded into Google BigQuery using the google-cloud-bigquery library.

## Notes
#### Ensure Docker is installed and running correctly on your machine.
#### The file challenge-borda-80fb1feb52cb.json must contain the appropriate credentials to access Google BigQuery.
#### Customize the docker-compose.yml and deploy.sh files as needed to fit your specific environment.

## License
####  This project is licensed under the MIT License. See the LICENSE file for more details.

```bash
Feel free to copy and paste this directly into your GitHub repository's `README.md` file.
```



