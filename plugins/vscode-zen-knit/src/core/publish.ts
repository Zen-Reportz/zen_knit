import * as vscode from 'vscode';
import path = require('path');
import { getCommand } from './command_line';
import cp = require('child_process');

export function knit(myChannel: vscode.OutputChannel){

    let build = vscode.commands.registerTextEditorCommand('vscode-zen-knit.build', async () => {

        if (vscode.window.activeTextEditor) {
            const currentDocument = vscode.window.activeTextEditor.document;
            const knit = await getCommand('knit');
            const d = new Date();

            myChannel.appendLine("processing: "+ currentDocument.uri.fsPath + " at: " + d.toISOString());
            cp.exec(knit + ' -f' + currentDocument.uri.fsPath, (error, stdout, stderr) => {
                myChannel.appendLine(stdout);
                myChannel.appendLine(stderr);
                if (error) {
                    myChannel.appendLine(error.message);
    
                    vscode.window.showErrorMessage("zen-knit : an error ocurred while building file");
                    return;
                }
                vscode.window.showInformationMessage("zen-knit : outputfile is build");
            });
        }
    })
    return build
}
