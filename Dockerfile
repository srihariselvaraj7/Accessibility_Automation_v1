
FROM python:3.14-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && python -m playwright install --with-deps chromium

# Copy the project files
COPY . .

# Create directories for generated reports and screenshots
RUN mkdir -p reports screenshots

# Run Playwright without opening a visible browser
ENV PLAYWRIGHT_HEADLESS=true

CMD ["python", "main.py"]
