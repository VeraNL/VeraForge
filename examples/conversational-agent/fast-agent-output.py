# EXAMPLE OUTPUT

from fast_agent.agent import Agent
from fast_agent.nodes import SensorNode, ProcessorNode, MemoryNode
from fast_agent.utils import *

class ConversationalCompanion(Agent):
    def __init__(self):
        super().__init__(
            name="ConversationalCompanion",
            essence=['Empathetic', 'Contextual', 'Adaptive'],
            purpose="To engage users in natural dialogue, remembering context and emotional tone across sessions."
        )

        # Channels
        self.VoiceInput = SensorNode("Microphone-V3")
        self.TextInput = SensorNode("TextBox-T1")
        self.EmotionEngine = ProcessorNode("ToneAnalyzer9000")
        self.LanguageModel = ProcessorNode("LLM-Core")

        # Memory
        self.DialogueMemory = MemoryNode(["UserHistory", "EmotionalState", "RecentTopics"])

        # Rituals
        self.add_ritual("EngageUser", self.EngageUser)
        self.add_ritual("RememberContext", self.RememberContext)

    def EngageUser(self, inputs):
        TextInput_Text = self.TextInput.read("Text")
        VoiceInput_Speech = self.VoiceInput.read("Speech")

        # Processing steps
        Transcribe(VoiceInput)                          # TODO: Implement or import
        MergeInputs(TextInput, VoiceInput)              # TODO: Implement or import
        AnalyzeTone(MergedInput) -> StoreTo(DialogueMemory)  # TODO: Implement or import
        GenerateResponse(MergedInput, EmotionalState)   # TODO: Implement or import
        OutputTo(LanguageModel)                         # TODO: Implement or import

        self.LanguageModel.send("Response", result)     # Final output placeholder

    def RememberContext(self, inputs):
        DialogueMemory_UserHistory = self.DialogueMemory.read("UserHistory")
        DialogueMemory_RecentTopics = self.DialogueMemory.read("RecentTopics")

        # Processing steps
        Summarize(RecentTopics)                         # TODO: Implement or import
        UpdateContextModel(UserHistory, SummarizedTopics)  # TODO: Implement or import
        OutputTo(LanguageModel)                         # TODO: Implement or import

        self.LanguageModel.send("Context", result)      # Final output placeholder