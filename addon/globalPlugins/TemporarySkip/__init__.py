# TemporarySkip main implementation
# Author: Yukio Nozawa <personal@nyanchangames.com>

import addonHandler
import api
import globalPluginHandler
import globalVars
import textInfos
import speech
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
		# Register with NVDA's speech extension point
		speech.extensions.filter_speechSequence.register(self._filterSpeechSequence)

	def terminate(self):
		# Unregister from the extension point
		speech.extensions.filter_speechSequence.unregister(self._filterSpeechSequence)

	def _filterSpeechSequence(self, speechSequence, *args, **kwargs):
		"""Filter speech sequence to remove skipped phrases."""
		if not self._skipped_phrases:
			return speechSequence
		filteredSequence = []
		for item in speechSequence:
			if isinstance(item, str):
				# Filter text strings by removing skipped phrases
				for phrase in self._skipped_phrases:
					item = item.replace(phrase, "")
				# Only add non-empty strings
				if item:
					filteredSequence.append(item)
			else:
				# Keep speech commands (like IndexCommand, etc.) as-is
				filteredSequence.append(item)
		return filteredSequence


	# define script
	@script(description=_("Toggle skip reading the selected phrase"), gesture="kb:nvda+f11")
	def script_skipSelectedPhrase(self, gesture):
		phrase = self._getPhraseFromMarkers()
		if phrase is None:
			return
		# end no phrase selected
		if phrase in self._skipped_phrases:
			self._skipped_phrases.remove(phrase)
			ui.message(_("%(phrase)s will be spoken") % {"phrase": phrase})
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
		ui.message(_("Everything will be spoken"))
