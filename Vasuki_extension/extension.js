const vscode = require('vscode');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Vasuki Language Extension is now active!');

    // Register the completion provider for Vasuki files
    const completionProvider = vscode.languages.registerCompletionItemProvider(
        'vasuki',
        {
            provideCompletionItems(document, position) {
                // Get the current line text up to the cursor position
                const linePrefix = document.lineAt(position).text.substr(0, position.character);
                
                // Define completion items for keywords
                const keywords = [
                    'if', 'else', 'while', 'for', 'return', 'yield', 'break', 'continue', 
                    'def', 'var', 'dynamic', 'true', 'false'
                ];
                
                // Define completion items for built-in functions
                const builtinFunctions = [
                    'print', 'length', 'push', 'pop',
                    'array_slice', 'array_join', 'array_sort', 'array_reverse', 'array_find', 
                    'array_find_last', 'array_count', 'array_unique',
                    'string_slice', 'string_match', 'string_search', 'string_replace', 
                    'string_split', 'string_match_all',
                    'sqrt', 'pow', 'log', 'log10', 'sin', 'cos', 'tan', 'asin', 'acos', 
                    'atan', 'atan2', 'degrees', 'radians',
                    'floor', 'ceil', 'round', 'abs', 'gcd', 'lcm', 'is_prime', 'factorial',
                    'random_int', 'random_float', 'random_uniform',
                    'bit_and', 'bit_or', 'bit_xor', 'bit_not', 'bit_shift_left', 'bit_shift_right',
                    'priority_queue', 'priority_queue_enqueue', 'priority_queue_dequeue', 
                    'priority_queue_peek', 'priority_queue_size', 'priority_queue_is_empty',
                    'set', 'set_add', 'set_remove', 'set_contains', 'set_clear', 'set_size', 
                    'set_to_list', 'set_union', 'set_intersection', 'set_difference', 
                    'set_is_subset', 'set_is_superset',
                    'is_int', 'is_float', 'is_string', 'is_char', 'is_bool',
                    'uppercase', 'lowercase', 'contains', 'startswith', 'endswith', 'replace', 'trim'
                ];
                
                // Create completion items
                const completionItems = [];
                
                // Add keyword completion items
                keywords.forEach(keyword => {
                    const item = new vscode.CompletionItem(keyword, vscode.CompletionItemKind.Keyword);
                    item.detail = 'Vasuki keyword';
                    completionItems.push(item);
                });
                
                // Add function completion items with documentation
                builtinFunctions.forEach(func => {
                    const item = new vscode.CompletionItem(func, vscode.CompletionItemKind.Function);
                    item.detail = 'Vasuki built-in function';
                    
                    // Add documentation for specific functions
                    switch (func) {
                        case 'print':
                            item.documentation = new vscode.MarkdownString('Prints a value to the console.\n\n`print(value);`');
                            break;
                        case 'length':
                            item.documentation = new vscode.MarkdownString('Returns the length of an array or string.\n\n`length(array);`');
                            break;
                        case 'push':
                            item.documentation = new vscode.MarkdownString('Adds an element to the end of an array.\n\n`push(array, element);`');
                            break;
                        case 'array_slice':
                            item.documentation = new vscode.MarkdownString('Returns a slice of an array (1-based indexing).\n\n`array_slice(array, start, end, step);`');
                            break;
                        case 'priority_queue':
                            item.documentation = new vscode.MarkdownString('Creates a new priority queue.\n\n`priority_queue(isMinQueue);` - Pass true for min queue, false for max queue');
                            break;
                        case 'set':
                            item.documentation = new vscode.MarkdownString('Creates a new set.\n\n`set();`');
                            break;
                        // Add more documentation as needed
                    }
                    
                    completionItems.push(item);
                });
                
                return completionItems;
            }
        }
    );
    
    // Register a hover provider for Vasuki files
    const hoverProvider = vscode.languages.registerHoverProvider(
        'vasuki',
        {
            provideHover(document, position, token) {
                const range = document.getWordRangeAtPosition(position);
                const word = document.getText(range);
                
                // Provide hover information for built-in functions
                switch (word) {
                    case 'print':
                        return new vscode.Hover('Prints a value to the console.\n\n`print(value);`');
                    case 'length':
                        return new vscode.Hover('Returns the length of an array or string.\n\n`length(array);`');
                    case 'push':
                        return new vscode.Hover('Adds an element to the end of an array.\n\n`push(array, element);`');
                    case 'array_slice':
                        return new vscode.Hover('Returns a slice of an array (1-based indexing).\n\n`array_slice(array, start, end, step);`');
                    case 'priority_queue':
                        return new vscode.Hover('Creates a new priority queue.\n\n`priority_queue(isMinQueue);` - Pass true for min queue, false for max queue');
                    case 'set':
                        return new vscode.Hover('Creates a new set.\n\n`set();`');
                    // Add more hover information as needed
                }
            }
        }
    );
    
    // Register a definition provider for Vasuki files
    const definitionProvider = vscode.languages.registerDefinitionProvider(
        'vasuki',
        {
            provideDefinition(document, position, token) {
                // This would provide "Go to Definition" functionality
                // For now, we'll just implement a simple version that finds function definitions
                
                const range = document.getWordRangeAtPosition(position);
                const word = document.getText(range);
                
                // Search for function definitions in the document
                const text = document.getText();
                const defRegex = new RegExp(`def\\s+${word}\\s*\\(`, 'g');
                let match;
                
                while ((match = defRegex.exec(text)) !== null) {
                    const pos = document.positionAt(match.index);
                    const line = document.lineAt(pos.line);
                    
                    return new vscode.Location(
                        document.uri,
                        new vscode.Range(pos, line.range.end)
                    );
                }
            }
        }
    );
    
    // Add the providers to the context subscriptions
    context.subscriptions.push(completionProvider);
    context.subscriptions.push(hoverProvider);
    context.subscriptions.push(definitionProvider);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
