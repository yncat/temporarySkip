# TemporarySkip main implementation
# Author: Yukio Nozawa <personal@nyanchangames.com>

import addonHandler
import gui
import globalPluginHandler
import globalVars
import threading
import time
import speech
import speechDictHandler
from logHandler import log
from scriptHandler import script

try:
	import addonHandler
	addonHandler.initTranslation()
except:
	_ = lambda x : x


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Temporary skip")

	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self._skipped_phrases = []
		if hasattr(speech, "speech"):
			self.processText_original = speech.speech.processText
		else:
			self.processText_original = speech.processText
		# end override

		def processText(locale, text, symbolLevel):
			text = self.processText_original(locale, text, symbolLevel)
			return text
		# end processText

		if hasattr(speech, "speech"):
			speech.speech.processText = processText
		else:
			speech.processText = processText
		# modify builtin speech dicts

	def _unhook(self):
		if hasattr(speech, "speech"):
			speech.speech.processText = self.processText_original
		else:
			speech.processText = self.processText_original


	# define script
	@script(description=_("Skip reading the selected phrase"), gesture="kb:nvda+f11")
	def script_skipSelectedPhrase(self, gesture):
		pass


	@script(description=_("Clear phrases to skip"), gesture="kb:nvda+shift+f11")
	def script_clearPhrasesToSkip(self, gesture):
		pass
