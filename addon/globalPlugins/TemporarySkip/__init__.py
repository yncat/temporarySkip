# TemporarySkip main implementation
# Author: Yukio Nozawa <personal@nyanchangames.com>

import addonHandler
import api
import globalPluginHandler
import globalVars
import textInfos
import threading
import speech
import time
import ui
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

	def _unhook(self):
		if hasattr(speech, "speech"):
			speech.speech.processText = self.processText_original
		else:
			speech.processText = self.processText_original


	# define script
	@script(description=_("Skip reading the selected phrase"), gesture="kb:nvda+f11")
	def script_skipSelectedPhrase(self, gesture):
		phrase = self._getPhraseFromMarkers()
		if phrase is None:
			return
		# end no phrase selected
		if phrase in self._skipped_phrases:
			ui.message(_("%(phrase)s will be spoken" % {"phrase": phrase}))
			self._skipped_phrases.remove(phrase)
		else:
			ui.message(_("%(phrase)s will be ignored") % {"phrase": phrase})
			self._skipped_phrases.append(phrase)
		# end toggle spoken or not spoken
		# Explicitly not clear the markers because I think it's more convenient


	def _getPhraseFromMarkers(self):
		# Mostly from the NVDA implementation, modified a bit
		pos = api.getReviewPosition().copy()
		if not getattr(pos.obj, "_copyStartMarker", None):
			ui.message(_("No start marker set"))
			return
		# end no start marker
		startMarker = api.getReviewPosition().obj._copyStartMarker
		copyMarker = startMarker.copy()
		# Check if the end position has moved
		if pos.compareEndPoints(startMarker, "endToEnd") > 0: # user has moved the cursor 'forward'
			# start becomes the original start
			copyMarker.setEndPoint(startMarker, "startToStart")
			# end needs to be updated to the current cursor position.
			copyMarker.setEndPoint(pos, "endToEnd")
			copyMarker.move(textInfos.UNIT_CHARACTER, 1, endPoint="end")
		else:# user has moved the cursor 'backwards' or not at all.
			# when the cursor is not moved at all we still want to select the character have under the cursor
			# start becomes the current cursor position position
			copyMarker.setEndPoint(pos, "startToStart")
			# end becomes the original start position plus 1
			copyMarker.setEndPoint(startMarker, "endToEnd")
			copyMarker.move(textInfos.UNIT_CHARACTER, 1, endPoint="end")
		# end cursor movement
		if copyMarker.compareEndPoints(copyMarker, "startToEnd") == 0:
			ui.message(_("No text selected"))
			api.getReviewPosition().obj._copyStartMarker = None
			return
		# end no text
		return copyMarker._get_text()

	@script(description=_("Clear phrases to skip"), gesture="kb:nvda+shift+f11")
	def script_clearPhrasesToSkip(self, gesture):
		self._skipped_phrases = []
		ui.message("Everything will be spoken")
