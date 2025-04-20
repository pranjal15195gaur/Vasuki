# Installing the Vasuki Language Extension

This guide explains how to install the Vasuki Language Extension for Visual Studio Code.

## Installation from the VS Code Marketplace

1. Open Visual Studio Code.
2. Go to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or by pressing `Ctrl+Shift+X`.
3. Search for "Vasuki Language".
4. Click on the "Install" button.
5. Once installed, any file with the `.vasuki` extension will automatically use the Vasuki language features.

## Manual Installation

If you have received the extension as a `.vsix` file, you can install it manually:

1. Open Visual Studio Code.
2. Go to the Extensions view by clicking on the Extensions icon in the Activity Bar or by pressing `Ctrl+Shift+X`.
3. Click on the "..." menu in the top-right corner of the Extensions view.
4. Select "Install from VSIX...".
5. Navigate to the location of the `.vsix` file and select it.
6. Click "Install".

## Verifying the Installation

To verify that the extension is installed correctly:

1. Create a new file with the `.vasuki` extension (e.g., `test.vasuki`).
2. Write some Vasuki code in the file.
3. Check that syntax highlighting is working correctly.
4. Try using code snippets by typing a snippet prefix (e.g., `def` for a function definition) and pressing `Tab`.
5. Hover over built-in functions to see documentation.

## Troubleshooting

If you encounter any issues with the extension:

1. Make sure you have the latest version of Visual Studio Code installed.
2. Try reloading the window (press `Ctrl+Shift+P`, type "Reload Window", and press Enter).
3. Check the "Output" panel (press `Ctrl+Shift+U`) and select "Vasuki Language" from the dropdown to see any error messages.
4. If the issue persists, please report it on the extension's GitHub repository.

## Uninstalling the Extension

To uninstall the extension:

1. Go to the Extensions view by clicking on the Extensions icon in the Activity Bar or by pressing `Ctrl+Shift+X`.
2. Find the Vasuki Language extension.
3. Click on the gear icon next to the extension.
4. Select "Uninstall".
5. Reload Visual Studio Code when prompted.
