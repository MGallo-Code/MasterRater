## **Dependencies**

Before running the project's setup script, ensure the following dependencies are installed on your system:

- **Python 3.7 or newer**:
  - Check your Python version:
    ```bash
    python3 --version
    ```
  - If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/).

---

# Project Setup

This project uses a virtual environment (`venv`) to manage dependencies. Occasionally, you may encounter issues running the program, particularly related to the **"cocoa" plugin** on macOS. Recreating the virtual environment often resolves these issues.

To simplify this process, we have included a `setup.sh` script. However, there are some constraints to be aware of based on your operating system and shell environment.

---

## **Supported Environments**

### macOS/Linux
The `setup.sh` script is fully supported on macOS and Linux systems with a standard Bash shell.

### Windows
On Windows, the `setup.sh` script **requires a Bash-compatible shell**, such as:
- [Git Bash](https://git-scm.com/downloads)
- [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install)

If you are not using a Bash-compatible shell (e.g., if you are using Command Prompt or PowerShell), the `setup.sh` script will not work. For these environments, a separate PowerShell script (`setup.ps1`) is provided.

---

## **Setup Instructions**

*These setup scripts create a new virtual environment, clean up any old environments, and install required python dependencies.*

### macOS/Linux
1. Open your terminal.
2. Run the following commands:
   ```bash
   chmod +x setup.sh  # Make the script executable
   ./setup.sh         # Run the setup script
   ```

### Windows (Command Prompt/PowerShell)
1. Open PowerShell.
2. Run the following command to execute the PowerShell setup script:
   ```powershell
   .\setup.ps1
   ```

---

## **Common Issues**

### "cocoa" Plugin Errors on macOS

If you encounter errors like:
```
qt.qpa.plugin: Could not find the Qt platform plugin “cocoa” in “”
This application failed to start because no Qt platform plugin could be initialized.
```

Recreating the virtual environment using the setup script (`setup.sh`) should resolve the issue.

---

## **Contributing**

Feel free to suggest any improvements by opening an issue or submitting a pull request.

---

## **License**

This project is licensd under the MIT License. See the [LICENSE file](https://github.com/MGallo-Code/CritiQit/blob/main/LICENSE) for details.