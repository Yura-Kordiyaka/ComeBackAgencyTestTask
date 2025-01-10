# Project Title

## Description

This FastAPI application allows users to review their GitHub repositories via the /review route. It uses AI to analyze
the code quality and provide feedback for improvement.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Docker
- Docker Compose

## Setup

To get started, follow these steps:

1. ** `.env` file** in the root directory of the **website_scrapper**:

   ```plaintext
   BASE_URL=https://ndis.gov.au/participants/using-your-plan
   PATH_OUTPUT_FILE=output_data
   CSS_SELECTOR=paragraph paragraph--type-section paragraph--view-mode-default ds-1col clearfix section__white

2. **Build and run the application** using Docker Compose. Execute the following command in your terminal in the **app**
   folder:

   ```bash
   docker-compose up --build

3. **after you run the docker, you will get the results in the output_data folder in the root folder of the project**