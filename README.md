# KtasExporter

A tool to automatically export your Codewars kata solutions to a local repository.

## Prerequisites

- Python 3.x
- Git
- Google Chrome

## Installation

1. Clone the repository:
```bash
git clone https://github.com/benjGam/KtasExporter.git
cd KtasExporter
```

2. Run the setup script:
- For Linux/MacOS:
  ```bash
  ./setup.sh
  ```
- For Windows:
  ```cmd
  setup.bat
  ```

3. Configure your environment:
   Create a `.env` file in the project root with the following variables:
   ```env
   MAIL_ADDRESS=your.email@example.com
   PASSWORD=your-codewars-password
   LOCAL_REPO_PATH=/path/to/save/katas
   KATA_FILE_NAME=katas.md
   USERNAME=your-codewars-username
   PUSH_STEP=10  # Number of katas to export per run
   ```

## Usage

### Linux/MacOS
After installation, you can use the tool in two ways:
1. Using the alias (requires terminal restart after installation):
   ```bash
   ktasexport
   ```
2. Using the run script directly:
   ```bash
   ./run.sh
   ```

### Windows
After installation, you can use the tool in two ways:
1. Using the command (requires terminal restart after installation):
   ```cmd
   ktasexport
   ```
2. Using the run script directly:
   ```cmd
   run.bat
   ```

## Disclaimer

⚠️ **Important**: To maintain the spirit of Codewars and respect the learning process of others:
- Always keep your kata solutions repository **private**
- Do not share your solutions publicly
- Use this tool for personal reference only

## What it does

1. Connects to your Codewars account
2. Retrieves your completed kata solutions
3. Saves them to the specified local repository
4. Automatically commits changes

## Features

- Automatic authentication
- Progressive kata extraction
- Automatic Git commits
- Duplicate prevention for already exported katas

## Troubleshooting

If you encounter ChromeDriver compatibility issues:
1. Check your Chrome version
2. Download the matching ChromeDriver version
3. Replace the driver in the `src/` directory

## Notes

- The tool uses a virtual environment for dependency management
- All credentials are stored locally in your `.env` file
- Git commits are automated for each kata export