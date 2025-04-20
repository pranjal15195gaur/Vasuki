#!/bin/bash

# Script to package the Vasuki Language Extension

echo "Packaging Vasuki Language Extension..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Package the extension
echo "Creating VSIX package..."
npx vsce package

echo "Done! The extension package has been created."
echo "You can install it in VS Code using the 'Install from VSIX...' option in the Extensions view."
