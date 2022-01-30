import * as vscode from 'vscode';
import { getCommand } from './command_line';
import cp = require('child_process');

const fullRange = (doc: vscode.TextDocument) => doc.validateRange(new vscode.Range(0, 0, Number.MAX_VALUE, Number.MAX_VALUE));

export function formatDoc(myChannel: vscode.OutputChannel){
    return vscode.languages.registerDocumentFormattingEditProvider('zen-knit-format', {
        async provideDocumentFormattingEdits(document: vscode.TextDocument): Promise<vscode.TextEdit[]> {
            console.log("hi inside");
            // const fullText = document.getText();
            // myChannel.appendLine(fullText)
            let finalDocument = "";
            // const autopep8Command = await getCommand('autopep8');
            // // let nowebReplace = fullText.replace(/(<<.*?>>=)(.*?)(@)/gms, (_, openingTag, code, closingTag) => {
            // let nowebReplace = fullText.replace(/(<<[^<>]*>>=)(.*?)(@)/gms, (_, openingTag, code, closingTag) => {
            //     let formattedPython = cp.execSync(autopep8Command + ' -', {
            //         input: code
            //     }).toString();
            //     return "\\begin{noweb}\n" + openingTag + formattedPython + closingTag + "\n\\end{noweb}";
            // });
            // const latexindentCommand = await getCommand('latexindent');
            // let indentedDocument = cp.execSync(latexindentCommand + ' -y="verbatimEnvironments:noweb:1', {
            //     input: nowebReplace
            // }).toString();
            // let finalDocument = indentedDocument.replace(/^\s*\\begin{noweb}.*?(<<.*?>>=.*?@).*?\\end{noweb}\h*$/gms, (_, code) => code);
            return [vscode.TextEdit.replace(fullRange(document), finalDocument)];
        }
    });

}