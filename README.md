# Markdown to Static Website Generator

This application converts markdown content into a static website. It processes markdown files, transforms them into HTML, and generates a structured static website based on the content.

## Features

- Converts markdown to HTML
- Generates a static website structure
- Easy to use with a simple bash script

## Prerequisites

- Python 3.x
- A web browser

## Installation

1. Clone this repository:
`git clone https://github.com/Antonvasilache/static-site-generator`
`cd static-site-generator`

2. No additional installation steps are required as the application uses Python's standard library.

## Usage

1. Place your markdown files in the `/content` directory. The structure of this directory will be reflected in the generated website.

2. Run the main script:
`./main.sh`

3. Open your web browser and navigate to `http://localhost:8888` to view your generated website.

## File Structure

- `/content`: Place your markdown files here
- `/src`: Contains the Python source code
- `/public`: The generated static website will be output here

## How It Works

1. The `main.py` script processes the markdown files in the `/content` directory.
2. It converts the markdown to HTML and generates the static website in the `/public` directory.
3. A Python HTTP server is started to serve the files from the `/public` directory.

## Customization

You can customize the appearance of your website by modifying the HTML templates and CSS files in the `/src` directory.