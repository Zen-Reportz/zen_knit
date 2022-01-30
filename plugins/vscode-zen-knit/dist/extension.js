/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ([
/* 0 */,
/* 1 */
/***/ ((module) => {

module.exports = require("vscode");

/***/ }),
/* 2 */
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.knit = void 0;
const vscode = __webpack_require__(1);
const command_line_1 = __webpack_require__(3);
const cp = __webpack_require__(5);
function knit(myChannel) {
    let build = vscode.commands.registerTextEditorCommand('vscode-zen-knit.build', async () => {
        if (vscode.window.activeTextEditor) {
            const currentDocument = vscode.window.activeTextEditor.document;
            const knit = await (0, command_line_1.getCommand)('knit');
            const d = new Date();
            myChannel.appendLine("processing: " + currentDocument.uri.fsPath + " at: " + d.toISOString());
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
    });
    return build;
}
exports.knit = knit;


/***/ }),
/* 3 */
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.getCommand = void 0;
const os = __webpack_require__(4);
const vscode = __webpack_require__(1);
const cp = __webpack_require__(5);
function getCommand(cmd) {
    const configuration = vscode.workspace.getConfiguration('zen-knit');
    const command = configuration.get(cmd + 'Path');
    return new Promise((resolve, reject) => {
        if (command === null || command === undefined) {
            reject(new Error(cmd + ' not defined in config'));
        }
        else {
            let checkCommand = "";
            switch (os.platform()) {
                case "win32":
                    checkCommand = 'where ' + command;
                    break;
                case "linux":
                case "darwin":
                    checkCommand = 'which ' + command;
            }
            cp.exec(checkCommand, (error, stdout, stderr) => {
                if (stdout !== "") {
                    resolve(command);
                }
                else {
                    reject(new Error(cmd + ' not defined in path'));
                }
            });
        }
    });
}
exports.getCommand = getCommand;


/***/ }),
/* 4 */
/***/ ((module) => {

module.exports = require("os");

/***/ }),
/* 5 */
/***/ ((module) => {

module.exports = require("child_process");

/***/ }),
/* 6 */
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.createchannel = void 0;
const vscode = __webpack_require__(1);
function createchannel() {
    return vscode.window.createOutputChannel("Zen-Knit");
}
exports.createchannel = createchannel;


/***/ }),
/* 7 */
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.formatDoc = void 0;
const vscode = __webpack_require__(1);
const fullRange = (doc) => doc.validateRange(new vscode.Range(0, 0, Number.MAX_VALUE, Number.MAX_VALUE));
function formatDoc(myChannel) {
    console.log("hi");
    return vscode.languages.registerDocumentFormattingEditProvider('zen-knit-format', {
        async provideDocumentFormattingEdits(document) {
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
exports.formatDoc = formatDoc;


/***/ })
/******/ 	]);
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
(() => {
var exports = __webpack_exports__;

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.deactivate = exports.activate = void 0;
const format_1 = __webpack_require__(7);
const knit_channel_1 = __webpack_require__(6);
const publish_1 = __webpack_require__(2);
function activate(context) {
    const mychannel = (0, knit_channel_1.createchannel)();
    mychannel.appendLine('vscode-zen-knit" is now active!');
    // // vscode.window.showInformationMessage('Zen Knit extension is activated');	
    // let disposable = vscode.commands.registerCommand('vscode-zen-knit.helloWorld', () => {
    // 	vscode.window.showInformationMessage('Hello World from vscode-zen-knit!');
    // });
    context.subscriptions.push((0, publish_1.knit)(mychannel));
    context.subscriptions.push((0, format_1.formatDoc)(mychannel));
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;

})();

module.exports = __webpack_exports__;
/******/ })()
;
//# sourceMappingURL=extension.js.map