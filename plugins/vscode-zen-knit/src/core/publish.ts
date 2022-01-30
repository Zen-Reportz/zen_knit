import * as vscode from 'vscode';
import path = require('path');
import { getCommand, getOutput } from './command_line';
import cp = require('child_process');
import * as fs from 'fs';

export function knit(myChannel: vscode.OutputChannel){

    let build = vscode.commands.registerTextEditorCommand('vscode-zen-knit.build', async () => {

        if (vscode.window.activeTextEditor) {
            const currentDocument = vscode.window.activeTextEditor.document;
            const knit = await getCommand('knit');
            var output = getOutput('f');
            let { dir: parentDir } = path.parse(currentDocument.uri.path);
            if (output === undefined){
                output = parentDir.toString()
            }
            const d = new Date();

            myChannel.appendLine("processing: "+ currentDocument.uri.fsPath + " at: " + d.toISOString());
            cp.exec(knit + ' -f ' + currentDocument.uri.fsPath + " -ofd " +  output, (error, stdout, stderr) => {
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
