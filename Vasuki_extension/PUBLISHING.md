# Publishing the Vasuki Language Extension

This guide explains how to package and publish the Vasuki Language Extension to the Visual Studio Code Marketplace.

## Prerequisites

1. Install Node.js and npm if you haven't already.
2. Install the Visual Studio Code Extension Manager (vsce):
   ```
   npm install -g @vscode/vsce
   ```
3. Create a Microsoft account if you don't have one.
4. Create an Azure DevOps organization: https://dev.azure.com/
5. Create a Personal Access Token (PAT) with the "Marketplace (publish)" scope.

## Packaging the Extension

1. Navigate to the extension directory:
   ```
   cd /path/to/Vasuki_extension
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Package the extension:
   ```
   vsce package
   ```
   This will create a `.vsix` file in the current directory.

## Testing the Packaged Extension

1. Open Visual Studio Code.
2. Go to the Extensions view (Ctrl+Shift+X).
3. Click on the "..." menu in the top-right corner of the Extensions view.
4. Select "Install from VSIX..." and choose the `.vsix` file you created.
5. Test the extension to make sure everything works as expected.

## Publishing to the Marketplace

1. Create a publisher on the Visual Studio Marketplace:
   - Go to https://marketplace.visualstudio.com/manage
   - Sign in with your Microsoft account
   - Create a new publisher if you don't have one

2. Update the `publisher` field in `package.json` to match your publisher ID.

3. Login to vsce with your Personal Access Token:
   ```
   vsce login <publisher-id>
   ```

4. Publish the extension:
   ```
   vsce publish
   ```

## Updating the Extension

1. Update the version number in `package.json`.
2. Update the CHANGELOG.md file with the changes.
3. Package and publish the extension as described above.

## Making the Extension Available to the Public

Once published, your extension will be available on the Visual Studio Code Marketplace. Users can install it by:

1. Opening Visual Studio Code
2. Going to the Extensions view (Ctrl+Shift+X)
3. Searching for "Vasuki Language"
4. Clicking "Install"

You can also share the direct link to your extension on the marketplace:
https://marketplace.visualstudio.com/items?itemName=<publisher-id>.vasuki-language

## Promoting Your Extension

To promote your extension:

1. Share it on social media
2. Create a GitHub repository for the extension
3. Add a link to the extension in your Vasuki language documentation
4. Create a demo video showing how to use the extension
5. Write a blog post about the extension and its features
