
import sublime
import sublime_plugin
import json
import subprocess
from string import Template


DEFAULT_LAYOUT = { "cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]]}
IO_PANE_LAYOUT = { "cols": [0.0, 0.5, 1.0], "rows": [0.0, 0.75, 0.75, 1.0], "cells": [[0, 0, 2, 1], [0, 2, 1, 3], [1, 1, 2, 3]]}
INPUT_VIEW_GROUP = 1
OUTPUT_VIEW_GROUP = 2

settings = sublime.load_settings("languages.sublime-settings")

class Environment(object):
	""" Environment for target file.

	Attributes:
		file_extension The extension of target file.
		file_base_name The base name of file (including extension).
		file_path      The path of file (without base name).
		file      The full file name including file_path, file_base_name and file_extension.
		platform       The name operating system underlying. (OSX, windows, Linux)

	"""
	file_extension = None
	file_base_name = None
	file_path = None
	file = None
	platform = None
	last_runnable_view = None

	@staticmethod
	def populate():
		variables = Environment.last_runnable_view.window().extract_variables()
		if "file_extension" in variables:
			Environment.file_extension = variables['file_extension']
		if "file_base_name" in variables:
			Environment.file_base_name = variables['file_base_name']
		if "file_path" in variables:
			Environment.file_path = variables['file_path']
		if "file" in variables:
			Environment.file = variables['file']
		if "platform" in variables:
			Environment.platform = variables['platform']


	@staticmethod
	def set_last_runnable_view(_last_runnable_view):
		Environment.last_runnable_view = _last_runnable_view
		Environment.populate()
		
class OutputFileEditCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		if("append" in args):
			self.view.insert(edit, self.view.size(), args["append"])
		if("erase" in args):
			self.view.erase(edit, sublime.Region(0, self.view.size()))
		

class Compiler(object):
	@staticmethod
	def compile(output_view):

		lang_settings = settings.get("lang-" + Environment.file_extension)
		if("compile_cmd" not in lang_settings):
			return 0

		compile_template = Template(lang_settings["compile_cmd"])
		compile_command = compile_template.substitute(code_file_extension=Environment.file_extension, code_file_base_name=Environment.file_base_name, code_file_path=Environment.file_path, code_file=Environment.file)

		output_view.run_command("output_file_edit", {"append" : "Compiling ...\n"});
		compile = subprocess.Popen(compile_command,
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        universal_newlines=True
                        )
		compile.wait();
		output_view.run_command("output_file_edit", {"append" : compile.args + "\n\n"});
		output,errors = compile.communicate()
		output_view.run_command("output_file_edit", {"append" : "\n" + output + "\n\n"});
		output_view.run_command("output_file_edit", {"append" : "Compilation finished with exit code : " + str(compile.returncode)});
		return compile.returncode


class Executor(object):
	def execute(input_view, output_view):
		lang_settings = settings.get("lang-" + Environment.file_extension)
		if("execute_cmd" not in lang_settings):
			return None


		execute_template = Template(lang_settings["execute_cmd"])
		execute_command = execute_template.substitute(code_file_extension=Environment.file_extension, code_file_base_name=Environment.file_base_name, code_file_path=Environment.file_path, code_file=Environment.file)

		output_view.run_command("output_file_edit", {"append" : "Running ...\n"});
		run = subprocess.Popen(execute_command,
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        universal_newlines=True
                        )
		output,errors = run.communicate(input_view.substr(sublime.Region(0, input_view.size())))
		run.wait();
		output_view.run_command("output_file_edit", {"append" : run.args + "\n\n"});
		output_view.run_command("output_file_edit", {"append" : "------------------------------------------\n"});
		output_view.run_command("output_file_edit", {"append" :  output + "\n"});
		output_view.run_command("output_file_edit", {"append" : "------------------------------------------\n"});
		output_view.run_command("output_file_edit", {"append" : "Execution finished with exit code : " + str(run.returncode)})
		

class CompileAndRunCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		output_view = Utils.create_output_file()

		if(Compiler.compile(output_view) != 0):
		 return None

		output_view.run_command("output_file_edit", {"erase" : "yup"});
		

		Executor.execute(self.view, output_view)



class Utils:
	@staticmethod
	def close_view(view):
		view.close()
	@staticmethod
	def close_views(views):
		for view in views:
			Utils.close_view(view)
	@staticmethod
	def close_group_files(group):
		Utils.close_views(sublime.active_window().views_in_group(group))


	@staticmethod
	def close_view_without_prompt(view):
		view.set_scratch(True)
		view.close()
	@staticmethod
	def close_views_without_prompt(views):
		for view in views:
			Utils.close_view_without_prompt(view)
	@staticmethod
	def close_group_files_without_prompt(group):
		Utils.close_views_without_prompt(sublime.active_window().views_in_group(group))


	@staticmethod
	def close_output_files():
		Utils.close_group_files_without_prompt(OUTPUT_VIEW_GROUP)
	@staticmethod
	def close_input_files():
		Utils.close_group_files(INPUT_VIEW_GROUP)


	@staticmethod
	def create_output_file():
		Utils.close_output_files();
		output_view = Utils.create_file_without_changing_focus()
		sublime.active_window().set_view_index(output_view, OUTPUT_VIEW_GROUP, 0)
		output_view.set_name("output")
		return output_view
	@staticmethod
	def create_file_without_changing_focus():
		current_focused_sheet = sublime.active_window().active_sheet()
		new_view = sublime.active_window().new_file()
		sublime.active_window().focus_sheet(current_focused_sheet)
		return new_view

class OpenInputOutputPaneCommand(sublime_plugin.TextCommand):
	"""docstring for OpenInputOutputPaneCommand"""
	def run(self, edit):
		sublime.active_window().set_layout(IO_PANE_LAYOUT)

		if len(sublime.active_window().views_in_group(INPUT_VIEW_GROUP)) == 0:
			input_view = Utils.create_file_without_changing_focus()
			sublime.active_window().set_view_index(input_view, INPUT_VIEW_GROUP, 0)
			input_view.set_name("Input")

		Utils.create_output_file()

class CloseInputOutputPaneCommand(sublime_plugin.TextCommand):
	"""docstring for CloseInputOutputPaneCommand"""
	def run(self, edit):
		Utils.close_input_files()
		Utils.close_output_files()
		sublime.active_window().set_layout(DEFAULT_LAYOUT)

class PluginEventListener(sublime_plugin.EventListener):
	"""docstring for PluginEventListener"""

	def on_activated(self, view):
		if sublime.active_window().active_group() == INPUT_VIEW_GROUP:
			None
		elif sublime.active_window().active_group() == OUTPUT_VIEW_GROUP:
			None
		else :
			Environment.set_last_runnable_view(view)

		