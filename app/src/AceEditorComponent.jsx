import React from 'react';
import AceEditor from 'react-ace';

import 'ace-builds/src-noconflict/mode-mysql';
import 'ace-builds/src-noconflict/theme-terminal';
import 'ace-builds/src-noconflict/ext-language_tools';

const AceEditorComponent = ({ initialCode, onCodeChange }) => {
    const handleChange = (newCode) => {
        if (onCodeChange) {
            onCodeChange(newCode);
        }
    };

    const handleLoad = (editor) => {
        console.log("i've loaded");
    };

    return (
        <div className="rounded-lg shadow-lg p-4 bg-white w-full">
            <AceEditor
                className="w-full"
                placeholder="DuckDB Editor"
                mode="mysql"
                theme="terminal"
                name="blah2"
                onLoad={handleLoad}
                onChange={handleChange}
                fontSize={14}
                showPrintMargin={true}
                showGutter={true}
                highlightActiveLine={true}
                value={initialCode}
                setOptions={{
                    enableBasicAutocompletion: true,
                    enableLiveAutocompletion: true,
                    enableSnippets: true,
                    showLineNumbers: true,
                    tabSize: 2,
                }}
                style={{ width: '100%' }}
            />
        </div>
    );
};

export default AceEditorComponent;
