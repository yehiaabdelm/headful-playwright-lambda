# Headful Playwright on Lambda

Ready-to-deploy solution for running Playwright in headful (non-headless) mode on AWS Lambda

- `app/app.py` - Lambda handler with the Xvfb configuration and Playwright code
- `app/Dockerfile` - Docker configuration with all necessary dependencies
- `app/requirements.txt` - Python dependencies including Playwright
- `template.yaml` - AWS SAM template for deployment

## Prerequisites

- AWS CLI configured with appropriate permissions
- SAM CLI installed
- Docker installed

## Development

Build the function

```bash
sam build
```

Start a server at port 3000. Just hit the function as shown in [Example Usage](#example-usage)

```bash
sam local start-api
```

## API Usage

The current function accepts POST requests with a JSON body to customize the screenshot. Customize this depending on your use case.

```json
{
  "url": "https://google.com",
  "width": 1920,
  "height": 1080
}
```

### Parameters

| Parameter | Type   | Required | Default              | Description               |
| --------- | ------ | -------- | -------------------- | ------------------------- |
| `url`     | string | No       | "https://google.com" | URL to capture            |
| `width`   | number | No       | 1280                 | Viewport width in pixels  |
| `height`  | number | No       | 720                  | Viewport height in pixels |

### Example Response

```json
{
  "message": "Screenshot taken successfully",
  "image_base64": "base64_encoded_image_data"
}
```

### Example Usage

```bash
# Using curl
curl -X POST \
  http://localhost:3000 \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://teletyped.com",
    "width": 1440,
    "height": 900
  }'
```

## Deployment

### Github Action

GitHub Actions workflow for automatic deployment on pushes to the main branch

1. Fork or clone this repository
2. Set up the following GitHub secrets in your repository settings:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key with deployment permissions
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
3. Optionally modify the AWS region in the workflow file (`.github/workflows/deploy.yml`)
4. Push changes to the main branch, and GitHub Actions will automatically build and deploy

```yaml
name: Build and deploy lambda function

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - uses: aws-actions/setup-sam@v1
      - uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-2

      - name: SAM build
        run: sam build

      - name: SAM deploy
        run: |
          sam deploy --no-fail-on-empty-changeset --no-confirm-changeset
```

## Configuration

See `template.yml` to configure your lambda's configuration.
