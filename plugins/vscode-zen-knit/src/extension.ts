'use strict';
import * as vscode from 'vscode';
import { formatDoc } from './core/format';
import { createchannel } from './core/knit_channel';
import { knit } from './core/publish';


export function activate(context: vscode.ExtensionContext) {

	const mychannel = createchannel()
	mychannel.appendLine('vscode-zen-knit" is now active!')

	// // vscode.window.showInformationMessage('Zen Knit extension is activated');	
	// let disposable = vscode.commands.registerCommand('vscode-zen-knit.helloWorld', () => {
	// 	vscode.window.showInformationMessage('Hello World from vscode-zen-knit!');
	// });

	context.subscriptions.push(knit(mychannel));

	context.subscriptions.push(formatDoc(mychannel));
}

// this method is called when your extension is deactivated
export function deactivate() {}
