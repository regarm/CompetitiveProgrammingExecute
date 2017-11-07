![Edge](https://i.imgur.com/q7rlhfw.png)
Sublime as IDE for competitive coding  
===============

## Features
 *  Separate pane for input and output in bottom
 *  Multiple input files for multiple test cases 
 *  Run just by keyboard shortcut
 *  Multiple languages (Default : C, C++, Java, Python)
 *  Add your own language


## Installation  
### Manual

1. Download the [latest release](https://github.com/regarmanojkumar/CompetitiveProgrammingExecute/releases/latest), extract and rename the directory to `package name`.
2. Move the directory inside your Sublime `/Packages` directory. *(Preferences > Browse packages...)*

## Keyboard shortcuts
Although, you can access these functionalities by right click on editor, here are the keymaps.

Default :  
	```[

   		{ "keys": ["ctrl+space+b"], "command": "compile_and_run" },
   		{ "keys": ["ctrl+space+o"], "command": "open_input_output_pane" },
   		{ "keys": ["ctrl+space+escape"], "command": "close_input_output_pane" }
   	]```

Keyboard shortcuts can be changed but make sure sublime or other package is not overriding them.
Edit respective file from following list :  
 * Default (Windows).sublime-keymap  
 * Default (OSX).sublime-keymap  
 * Default (Linux).sublime-keymap  


## Integrate your own language
You can add your own language to the list in ```Languages.sublime-settings```

Here is the example of default ```Languages.sublime-settings```.  


~~~  
{
	"lang-c" : {
		"compile_cmd" : "gcc \"${code_file}\" -o \"${code_file_path}/${code_file_base_name}\"",
		"execute_cmd" : "\"${code_file_path}/${code_file_base_name}\""
	},
	"lang-cpp" : {
		"compile_cmd" : "g++ \"${code_file}\" -o \"${code_file_path}/${code_file_base_name}\"",
		"execute_cmd" : "\"${code_file_path}/${code_file_base_name}\""
	},
	"lang-java" : {
		"compile_cmd" : "javac \"${code_file}\"",
		"execute_cmd" : "java -cp \"${code_file_path}\" Main"
		},
	"lang-py" : {
		"execute_cmd" : "python \"${code_file}\""
	}
}
~~~

The key ```lang-extension``` is used to determine which language command should be used.  
Following variables are available :  
 * ${code_file_extension} : Extension of file being executed.  
 * ${code_file_base_name} : Base file name of file being executed.  
 * ${code_file_path} : Full path of file being executed (excluding name and extension).  
 * ${code_file} : Full path of file being executed (including name and extension).  

i.e. If your program file is ```/Users/regar/file.cpp```, then
 *  ${code_file_extension} : cpp  
 *  ${code_file_base_name} : file  
 *  ${code_file_path} : /Users/regar  
 *  ${code_file} : /Users/regar/file.cpp  
 
 ## Bugs / Issues / Features requests

Please file bugs / feature requests by filing an issue to the project or send an email to ```regarmanojkumar@gmail.com``` 


## Get involved  
Fork, develop and make a merge request. 
