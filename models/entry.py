class Entry():
    """_summary_
    """
    def __init__(self, id, concept, entry, date, mood_id, mood = None, tags = None):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.date = date
        self.mood_id = mood_id
        self.mood = mood
        self.tags = tags
